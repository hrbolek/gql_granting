import json
import strawberry
from src.GraphTypeDefinitions import schema

from graphql import parse
from graphql.language.ast import (
    DocumentNode,
    InputObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    NamedTypeNode,
    ListTypeNode,
    NonNullTypeNode,
)

def graphql_type_to_json(type_node):
    """
    Převede GraphQL typové uzly na JSON Schema fragment.
    Podporuje NamedType, List, NonNull a mapuje základní scalary i custom scalary.
    """
    # unwrap NonNull
    if isinstance(type_node, NonNullTypeNode):
        return graphql_type_to_json(type_node.type)
    # list => array or null
    if isinstance(type_node, ListTypeNode):
        item_schema = graphql_type_to_json(type_node.type)
        return {"type": ["array", "null"], "items": item_schema}
    # NamedType
    if isinstance(type_node, NamedTypeNode):
        name = type_node.name.value
        # základní scalars
        if name in ("String", "ID"):
            return {"type": ["string", "null"]}
        if name == "Int":
            return {"type": ["integer", "null"]}
        if name == "Float":
            return {"type": ["number", "null"]}
        if name == "Boolean":
            return {"type": ["boolean", "null"]}
        # custom scalars
        if name == "UUID":
            return {"type": ["string", "null"], "format": "uuid"}
        # jiný input object
        return {"$ref": f"#/definitions/{name}"}
    return {"type": ["array", "null"], "items": item_schema}
   
def build_json_schema(ast: DocumentNode, root: str, oneof=True) -> dict:
    """
    Z AST GraphQL SDL vytvoří JSON Schema pro InputObject root.
    Rekurzivně sestaví definitions a properties.
    Podporuje @oneOf direktivu pro vynucení právě jedné vlastnosti.
    """
    # map input definitions
    inputs = {
        d.name.value: d
        for d in ast.definitions
        if isinstance(d, (InputObjectTypeDefinitionNode, ScalarTypeDefinitionNode))
    }
    if root not in inputs:
        raise ValueError(f"Typ {root} není InputObject v SDL")
    root_node = inputs[root]
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": root,
        "type": "object",
        "description": getattr(root_node, "description", None) and root_node.description.value,
        "properties": {},
        "definitions": {},
        "additionalProperties": False,
    }

    def process(name: str):
        if name in schema["definitions"]:
            return
        schema["definitions"][name] = {}
        node = inputs.get(name)
        props = {}
        for f in node.fields or []:
            fname = f.name.value
            js = graphql_type_to_json(f.type)
            if f.description:
                js["description"] = f.description.value
            props[fname] = js
            # pokud $ref, rozděl rekurzi
            # přímý odkaz
            ref = js.get("$ref")
            # nebo odkaz uvnitř položky items (pro listy)
            if not ref and isinstance(js, dict) and "items" in js:
                items = js.get("items")
                if isinstance(items, dict) and "$ref" in items:
                    ref = items.get("$ref")
            if ref:
                # odstranění prefixu '#/definitions/'
                ref_name = ref.split("/")[-1]
                process(ref_name)
        entry = {
            "type": "object",
            "description": getattr(node, "description", None) and node.description.value,
            "properties": props,
            "additionalProperties": False,
        }
        # direktiva oneOf
        # directives = getattr(node, 'directives', [])
        # if any(d.name.value == 'oneOf' for d in directives):
        if oneof:
            one_of = []
            for f in node.fields or []:
                one_of.append({"required": [f.name.value], "maxProperties": 1})
            entry["oneOf"] = one_of
        schema["definitions"][name] = entry

    # vytvor definitions pro root
    process(root)
    # proprties = root definition's properties
    schema["properties"] = schema["definitions"][root]["properties"]
    return schema

def unwrap_str_type(t):
    # if this is Optional[T] or List[T], recurse into the inner T
    if hasattr(t, "of_type"):
        return unwrap_str_type(t.of_type)
    return t

def build_validation_skill(schema, where):
    import jsonschema
    # from semantic_kernel.skill_definition import sk_native_function
    json_schema_for_where = build_json_schema(schema, where)
    print(json_schema_for_where)
    # @sk_native_function(
    #     name=f"ValidateFilter {where.name}",
    #     description="Transforms natural language filter criteria into a structured JSON object conforming to the ProgramInputFilter schema, supporting logical operators (_or, _and) and field filters (id, name)",
    #     parameter_schema=json_schema_for_where)
    def validate_filter(json_str: str) -> str:
        # SK vygeneruje validní JSON
        as_json = json.loads(json_str) if isinstance(json_str, dict) else json_str
        jsonschema.validate(as_json, json_schema_for_where)
        return json.dumps()
    
    return validate_filter

def skills_from_schema(schema, kernel=None):
    # from semantic_kernel import Kernel
    # _kernel = Kernel() if kernel is None else kernel
    typed_schema: strawberry.federation.Schema = schema
    query_type = typed_schema.get_type_by_name("Query")
    query_fields = query_type.fields
    # filter_field = lambda field: field.python_name.startswith("program_page")
    filter_pages = lambda field: field.python_name.endswith("page")
    filtered = (field for field in query_fields if filter_pages(field))
    for resolver in filtered:
        arguments = resolver.arguments
        filtered_arguments = (argument for argument in arguments if argument.python_name == "where")
        where = next(filtered_arguments, None)
        where = unwrap_str_type(where.type)
        skill = build_validation_skill(schema, where)
        break
        if kernel:
            kernel.import_skill(skill, skill_name=f"FilterValidation {where.name}")
    return kernel
    

# from src.GraphTypeDefinitions.Program.ProgramGQLModel import ProgramQuery
# local_schema = strawberry.federation.Schema(ProgramQuery)
# sdl = local_schema.as_str()
sdl = schema.as_str()

# skills_from_schema(schema)
ast = parse(sdl)
name = "ProgramInputFilter"
jschema = build_json_schema(ast, name)
print(json.dumps(jschema, indent=2))
with open("localschema.json", "w+", encoding="utf-8") as f:
    json.dump(jschema, f, indent=4)

with open("localschema.graphql", "w+", encoding="utf-8") as f:
    f.writelines(sdl)