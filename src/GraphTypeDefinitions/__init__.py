import strawberry
from .BaseGQLModel import IDType

from .Plan import PlanQuery, PlanMutation
from .Program import ProgramQuery, ProgramMutation
from .Student import StudentQuery, StudentMutation

from .DocumentGQLModel import DocumentGQLModel
from .EventGQLModel import EventGQLModel
from .GroupGQLModel import GroupGQLModel
from .UserGQLModel import UserGQLModel

@strawberry.type(description="""Type for query root""")
class Query(
    ProgramQuery, 
    StudentQuery, 
    PlanQuery
):
    pass


@strawberry.type(description="root of mutations")
class Mutation(
    ProgramMutation,
    StudentMutation,
    PlanMutation
):
    pass

schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[],
    types=[DocumentGQLModel, EventGQLModel, GroupGQLModel, UserGQLModel]
)

from uoishelpers.schema import WhoAmIExtension
schema.extensions.append(WhoAmIExtension)

from typing import Dict, Any, Optional
from strawberry.extensions import Extension
from graphql import DocumentNode, OperationDefinitionNode, FieldNode
from graphql import parse
# =====================================================
# 4. Funkce pro parsování AST dotazu – získání dotazovaných polí
# =====================================================

def get_nested_fields(field_node: FieldNode) -> Dict[str, Any]:
    nested = {}
    if field_node.selection_set:
        for sel in field_node.selection_set.selections:
            print(f"selection: {sel.to_dict()}")
            if sel.kind.lower() == "field":
                nested[sel.name.value] = get_nested_fields(sel)
    return nested

def get_requested_fields(document: DocumentNode) -> Dict[str, Any]:
    requested = {}
    for definition in document.definitions:
        if isinstance(definition, OperationDefinitionNode):
            for selection in definition.selection_set.selections:
                print(f"selection: {selection.to_dict()}")
                if selection.kind.lower() == "field":
                    requested[selection.name.value] = get_nested_fields(selection)
    return requested

# =====================================================
# 5. Funkce pro dynamickou extrakci stromu typu na základě dotazu
# =====================================================

def extract_type_structure(
    type_obj: Any, 
    requested_fields: Optional[Dict[str, Any]] = None, 
    depth: int = 0
) -> Dict[str, Any]:
    """
    Rekurzivně zmapuje strukturu dataclass (např. Strawberry typ Item)
    a vrátí slovník obsahující pouze dotazovaná pole (podle requested_fields).
    Pokud requested_fields je None, zahrne všechna pole.
    """
    indent = "  " * depth
    structure = {"type": str(type_obj)}
    origin = getattr(type_obj, "__origin__", None)
    
    if origin:
        structure["origin"] = str(origin)
        if origin in {list, tuple, set, frozenset}:
            inner = type_obj.__args__[0]
            structure["inner"] = extract_type_structure(inner, requested_fields, depth + 1)
        elif origin is dict:
            key_type, value_type = type_obj.__args__
            structure["key"] = str(key_type)
            structure["value"] = extract_type_structure(value_type, requested_fields, depth + 1)
        else:
            structure["args"] = [extract_type_structure(arg, requested_fields, depth + 1)
                                   for arg in type_obj.__args__ if arg is not type(None)]
    elif hasattr(type_obj, "__annotations__"):
        fields = {}
        for field_name, field_type in type_obj.__annotations__.items():
            if requested_fields is not None and field_name not in requested_fields:
                continue
            nested_requested = requested_fields.get(field_name) if requested_fields else None
            field_structure = extract_type_structure(field_type, nested_requested, depth + 1)
            fields[field_name] = field_structure
        structure["fields"] = fields
    # logging.info(f"{indent}Extracted: {structure}")
    print(f"{indent}Extracted: {structure}")
    return structure


# =====================================================
# 7. Schema Extension – generování SQL dotazu při dotazu
# =====================================================

class SQLQueryExtension(Extension):
    def on_request_start(self) -> None:
        """
        Při startu požadavku:
         1. Získáme AST dotazu a vyextrahujeme požadovaná pole.
         2. Na základě požadovaných polí vytvoříme strom typu (extract_type_structure).
         3. Sestavíme SQLAlchemy dotaz podle stromu a vstupního filtru.
         4. Dotaz vykonáme, převedeme výsledky na JSON a uložíme do contextu.
        """
        # Získáme GraphQL dotaz jako string
        query_string: str = self.execution_context.query

        # Pokud není žádný dotaz (např. introspekce), neděláme nic
        if not query_string:
            return

        # Parsujeme dotaz na AST
        document: DocumentNode = parse(query_string)
        requested_fields = get_requested_fields(document)
        print(f"Requested fields: {requested_fields}")
       

        operation = next(filter(lambda d: isinstance(d, OperationDefinitionNode), document.definitions))
        print(f"Filtered type tree: {document.definitions[0]}")
        print(f"Filtered type tree: {operation.to_dict()}")
        

# schema.extensions = [SQLQueryExtension, WhoAmIExtension]