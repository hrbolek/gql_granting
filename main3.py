from graphql import parse
from graphql.language.ast import (
    DocumentNode,
    InputObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    NamedTypeNode,
    ListTypeNode,
    NonNullTypeNode,
)
from graphql.language.printer import print_ast

from jinja2 import Template

TYPEDICTS_TEMPLATE = """
from typing import TypedDict, Optional, List, Any, Annotated
import uuid
import datetime

{% for name, fields in input_objects.items() %}
class {{ name }}(TypedDict, total=False):
{% if fields %}
{% for field in fields %}
    {% if field.description -%}# {{ field.description }}{% endif %}
    {{ field.name }}: {{ field.type }}
{% endfor %}
{% else %}
    pass
{% endif %}

{% endfor %}
"""

SKILL_TEMPLATE = '''
from semantic_kernel.functions import kernel_function
import requests
import json

@kernel_function(
    # description="{{ kernel_description }}"
)
def {{ func_name }}(
    {%- for arg in args %}
    {{ arg.name }}: {% if arg.description %}Annotated[{{ arg.type }}, "{{ arg.description }}"]{% else %}{{ arg.type }}{% endif %}{% if arg.default is not none %} = {{ arg.default }}{% endif %}{% if not loop.last %},{% endif %}
    {%- endfor %}, 
    context: dict = None
) -> {{ output_typename }}:
    """
    {{ kernel_description }}
    {{ field_description }}
    

    Parameters:
    {% for arg in args %}
    - {{ arg.name }} ({{ arg.type }}){% if not arg.required %}, optional{% endif %}: {{ arg.description or "Viz SDL" }}
    {% endfor %}
    Returns: {{ output_typename }}
    """
    endpoint = "{{ graphql_endpoint }}"
    query = """
    {{ graphql_query }}
    """
    variables = {
        {% for arg in args -%}
        "{{ arg.name }}": {{ arg.name }}{% if not loop.last %}, {% endif %}
        {%- endfor %}
    }
    response = requests.post(endpoint, json={"query": query, "variables": variables})
    response.raise_for_status()
    rows = response.json()
    assert "data" in rows, f"the response does not contain the data key {rows}"
    data = rows["data"]
    return [{{main_output_typename}} (**x) for x in data["{{ field_name }}"]]
    # return {{ output_typename }}(**response.json()["data"]["{{ field_name }}"])
'''

from graphql import parse
from graphql.language.ast import ObjectTypeDefinitionNode

def get_inner_typename(type_node):
    # Odstripuje List a NonNull až k NamedTypeNode, vrátí jméno typu
    t = type_node
    while isinstance(t, (NonNullTypeNode, ListTypeNode)):
        t = t.type
    if isinstance(t, NamedTypeNode):
        return t.name.value
    return None

def find_field_definition(ast, operation, field_name):
    # najde field podle názvu
    for defn in ast.definitions:
        if isinstance(defn, ObjectTypeDefinitionNode) and defn.name.value == operation:
            for f in defn.fields:
                if f.name.value == field_name:
                    return f
    raise ValueError(f"Field {field_name} not found in {operation}")

def get_python_main_output_type(type_node, outputs_map):
    # Odstripuje List a Optional/NonNull až k NamedTypeNode, vrátí jméno pro konstruktor
    t = type_node
    while isinstance(t, (NonNullTypeNode, ListTypeNode)):
        t = t.type
    if isinstance(t, NamedTypeNode):
        name = t.name.value
        if name in outputs_map:
            return name
        return name  # fallback, pokud není v outputs_map
    return "Any"

def gql_default_value_to_python(ast_value):
    # Pro jednoduché hodnoty (Int, Float, String, Boolean, Enum, Null, List)
    if ast_value is None:
        return None
    from graphql.language import ast as gqlast
    if isinstance(ast_value, gqlast.IntValueNode):
        return ast_value.value
    if isinstance(ast_value, gqlast.FloatValueNode):
        return ast_value.value
    if isinstance(ast_value, gqlast.StringValueNode):
        return f'"{ast_value.value}"'
    if isinstance(ast_value, gqlast.BooleanValueNode):
        return "True" if ast_value.value else "False"
    if isinstance(ast_value, gqlast.EnumValueNode):
        return f'"{ast_value.value}"'
    if isinstance(ast_value, gqlast.NullValueNode):
        return "None"
    if isinstance(ast_value, gqlast.ListValueNode):
        # Rekurzivně zpracuj hodnoty v poli
        return "[" + ", ".join([str(gql_default_value_to_python(v)) for v in ast_value.values]) + "]"
    # Pro další typy (ObjectValueNode, VariableNode, ...) přidej další větve dle potřeby
    return print_ast(ast_value)

def gql_type_to_python(type_node, inputs_map) -> str:
    if isinstance(type_node, NonNullTypeNode):
        return gql_type_to_python(type_node.type, inputs_map)
    if isinstance(type_node, ListTypeNode):
        return f"List[{gql_type_to_python(type_node.type, inputs_map)}]"
    if isinstance(type_node, NamedTypeNode):
        name = type_node.name.value
        mapping = {
            "String": "str",
            "ID": "str",
            "Int": "int",
            "Float": "float",
            "Boolean": "bool",
            "UUID": "uuid.UUID",   
            "DateTime": "datetime.datetime", 
        }
        if name in mapping:
            return mapping[name]
        if name in inputs_map:
            return f'"{name}"'
        return "Any"
    return "Any"

def collect_all_input_objects(ast, arg_type_nodes):
    """
    Najde všechny InputObjectTypeDefinitionNode (rekurzivně) pro _všechny_ vstupní typy argumentů field-u.
    """
    inputs_map = {
        d.name.value: d
        for d in ast.definitions
        if isinstance(d, InputObjectTypeDefinitionNode)
    }
    result = {}

    def visit(name):
        if name in result or name not in inputs_map:
            return
        result[name] = "placeholder to avoid cycle"
        node = inputs_map[name]
        fields = []
        for f in node.fields or []:
            field_type = gql_type_to_python(f.type, inputs_map)
            desc = f.description.value if f.description else None
            inner_typename = get_inner_typename(f.type)
            if inner_typename in inputs_map:
                visit(inner_typename)
            is_nonnull = isinstance(f.type, NonNullTypeNode)
            typ = field_type if is_nonnull else f"Optional[{field_type}]"
            fields.append({"name": f.name.value, "type": typ, "description": desc})
        result[name] = fields

    for type_node in arg_type_nodes:
        # odstraň NonNullType a ListType, chceme název typu
        t = type_node
        while isinstance(t, (NonNullTypeNode, ListTypeNode)):
            t = t.type
        if isinstance(t, NamedTypeNode):
            visit(t.name.value)
    return result

def gql_output_type_to_python(type_node, outputs_map) -> str:
    if isinstance(type_node, NonNullTypeNode):
        return gql_output_type_to_python(type_node.type, outputs_map)
    if isinstance(type_node, ListTypeNode):
        return f"List[{gql_output_type_to_python(type_node.type, outputs_map)}]"
    if isinstance(type_node, NamedTypeNode):
        name = type_node.name.value
        mapping = {
            "String": "str",
            "ID": "str",
            "Int": "int",
            "Float": "float",
            "Boolean": "bool",
            "UUID": "uuid.UUID",   
            "DateTime": "datetime.datetime", 
        }
        if name in mapping:
            return mapping[name]
        if name in outputs_map:
            return f'"{name}"'
        return "Any"
    return "Any"

def collect_all_output_objects(ast, root_type_node):
    outputs_map = {
        d.name.value: d
        for d in ast.definitions
        if isinstance(d, ObjectTypeDefinitionNode)
    }
    result = {}

    def visit(name):
        if name in result or name not in outputs_map:
            return
        result[name] = "placeholder to avoid cycle"
        node = outputs_map[name]
        fields = []
        for f in node.fields or []:
            field_type = gql_output_type_to_python(f.type, outputs_map)
            desc = f.description.value if f.description else None
            inner_typename = get_inner_typename(f.type)
            if inner_typename in outputs_map:
                visit(inner_typename)
            is_nonnull = isinstance(f.type, NonNullTypeNode)
            typ = field_type if is_nonnull else f"Optional[{field_type}]"
            fields.append({"name": f.name.value, "type": typ, "description": desc})
        result[name] = fields

    t = root_type_node
    while isinstance(t, (NonNullTypeNode, ListTypeNode)):
        t = t.type
    if isinstance(t, NamedTypeNode):
        visit(t.name.value)
    return result, t.name.value if isinstance(t, NamedTypeNode) else "Any"

def generate_kernel_skill(
    ast: DocumentNode, 
    operation: str, 
    field_name: str, 
    graphql_endpoint: str=""
):   
    field = find_field_definition(ast, operation, field_name)
    field_description = field.description.value if getattr(field, "description", None) else ""
    # ----- VSTUPNÍ TYPY -----
    arg_defs = field.arguments
    arg_type_nodes = [a.type for a in arg_defs]
    input_objects = collect_all_input_objects(ast, arg_type_nodes)

    # vstupní argumenty
    inputs_map = {
        d.name.value: d
        for d in ast.definitions
        if isinstance(d, InputObjectTypeDefinitionNode)
    }
    args = []
    for a in arg_defs:
        typ = gql_type_to_python(a.type, inputs_map)
        desc = a.description.value if a.description else None
        is_nonnull = isinstance(a.type, NonNullTypeNode)
        # Default: podle AST nebo None
        default = None
        if hasattr(a, "default_value") and a.default_value is not None:
            default = gql_default_value_to_python(a.default_value)
        elif not is_nonnull:
            default = "None"
        args.append({
            "name": a.name.value, 
            "type": typ, 
            "description": desc, 
            "required": is_nonnull,
            "default": default
        })

    needs_uuid_in = any("UUID" in field["type"] for fields in input_objects.values() for field in fields)
    typedicts_code_in = Template(TYPEDICTS_TEMPLATE).render(
        input_objects=input_objects, 
        needs_uuid=needs_uuid_in
    )

    # ----- VÝSTUPNÍ TYPY -----
    output_objects, _ = collect_all_output_objects(ast, field.type)
    needs_uuid_out = any("UUID" in field["type"] for fields in output_objects.values() for field in fields)
    typedicts_code_out = Template(TYPEDICTS_TEMPLATE).render(
        input_objects=output_objects, 
        needs_uuid=needs_uuid_out and not needs_uuid_in
    )
    main_output_typename = get_python_main_output_type(field.type, output_objects)
    # --- DŮLEŽITÉ! Získání přesné Python anotace návratového typu ---
    output_typename = gql_output_type_to_python(field.type, output_objects)

    # ---- Vygeneruj kernel skill ----
    kernel_description = f"Automaticaly generated skill for acces to graphql endpoint from sdl for {operation}.{field_name}."
    graphql_query = f"{field_name}(...)"  # zde bys vygeneroval konkrétní GQL dotaz podle input typů
    skill_code = Template(SKILL_TEMPLATE).render(
        kernel_description=kernel_description,
        func_name=field_name,
        args=args,
        operation_type=operation,
        field_name=field_name,
        field_description=field_description,
        graphql_endpoint=graphql_endpoint,
        graphql_query=graphql_query,
        output_typename=output_typename,
        main_output_typename=main_output_typename,
        input_fields=args,  # aby měl docstring správný popis
    )

    # Výsledný .py soubor
    code = f"{typedicts_code_in}\n\n{typedicts_code_out}\n\n{skill_code}"
    return code



from src.GraphTypeDefinitions import schema
sdl = schema.as_str()

# skills_from_schema(schema)
ast = parse(sdl)
python_code = generate_kernel_skill(
    ast=ast,
    operation="Query",
    field_name="studentPage"
)

output_file = "./__code.py"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(python_code)
