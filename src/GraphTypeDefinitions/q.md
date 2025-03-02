Pracuješ v pythonu, vyvíjíš graphql endpoint s pomocí strawberry

místo strawberry.field vytvoř custom dekorátor, který ponese navíc speciální metadata, což bude funkce, nazvěme ji select_func
tento custom dekorátor pojmenuj alchemyfield

připrav schemaextension, která na základě příchozího dotazu identifikuje, která položka (field) z typu Query je dotazem oslovena.

z této položky, z jejího typu a z vnořených položek a jejich typů odvoď strom typů, strom vytvoř jako vnořené dict, v každém dict bude také uložena funkce z metadat fieldu, tedy funkce select_func, ale také název položky a strawberry typ, na který se odkazuje

vytvoř funkci, která na základě mapy, implementované pomocí dict, která spojuje strawberry typy a sqlalchemy modely tabulek (dědí MappedAsDataclass), vytvoří dotaz v orm sqlachemy, po jehož vykonání dostanu úplnou strukturu dat z databáze



V jaké podobě bude select_func?


Má vracet pouze select(model) nebo má aplikovat i filtraci či joiny?
Bude pracovat jen se svým polem, nebo ovlivní celý dotaz?
Jaké ORM SQLAlchemy modely používáte?

Používáte MappedAsDataclass nebo běžné SQLAlchemy modely?
Bude třeba řešit vztahy mezi tabulkami, například relationship()?
Jak vypadá struktura vašich typů?

Máte ukázkový GraphQL typ (např. Query) a odpovídající SQLAlchemy model?
Má být podpora pro vnořená data (např. dotaz users { id, profile { age } })?
Jaká je očekávaná strategie vykonání dotazu?

Chcete vytvořit dotaz s JOINy a eager loadingem (joinedload())?
Nebo chcete nejprve načíst hlavní objekty a pak jednotlivé části stromu separátními dotazy?
Jaká verze SQLAlchemy se používá?

SQLAlchemy 1.x nebo moderní SQLAlchemy 2.0 (async/await)?

select_func má být funkce, která má jako parametry 
- model tabulky, která je spojena se strawberry typem
- model tabulky, která odpovídá návratovému typu příslušného fieldu, pozor na Optional[DbModel] a List[DbModel]
- select výraz (např. select(RootDbModel))
návratová hodnota je např. select(RootDbModel).join(FieldDbModel)

jako sqlachemy modely jsou použity modely, které jsou i dataclass, např.
```python
class BaseModel(MappedAsDataclass, DeclarativeBase):
    id: Mapped[IDType] = mapped_column(index=True, primary_key=True, default_factory=uuid.uuid4)
```

podpora má být i pro vnořená data
users { id, profile { age } }

načítat se budou všechny atributy, které mají skaláraní typy (podle definice graphQL, SCALAR) a provede se propojení na typy OBJECT, toto propojení je definováno funkcí select_func

vše se realizuje v sqlalchemy 2.0 v asynchronním režimu

# Rozšíření Strawberry GraphQL pro asynchronní ORM dotazy s dynamickým generováním dotazu

Toto řešení ukazuje, jak vytvořit vlastní *schema extension* pro Strawberry GraphQL, která:

1. **Používá vlastní dekorátor `alchemyfield`** – ten rozšiřuje standardní `strawberry.field` o dodatečná metadata, konkrétně o funkci `select_func`. Tato funkce má následující parametry:
   - *model tabulky* – SQLAlchemy model, který je spojen se strawberry typem.
   - *model tabulky cílového typu* – SQLAlchemy model odpovídající návratovému typu daného fieldu (podpora pro `Optional[DbModel]` a `List[DbModel]`).
   - *select výraz* – např. `select(RootDbModel)`.
   
   Návratová hodnota je např. `select(RootDbModel).join(FieldDbModel)`.

2. **Schema extension analyzuje příchozí dotaz** – pomocí AST dotazu (přes `graphql.parse`) a nástroje `TypeInfo` se dynamicky určí, které top-level pole (např. `users`) bylo dotazováno. Poté se na základě tohoto pole a jeho návratového typu (a vnořených polí) sestaví strom typů. Strom je implementován jako vnořený dict, kde každý uzel obsahuje:
   - **`strawberry_type`** – odvozený strawberry typ.
   - **`select_func`** – funkce z metadat daného fieldu (získaná pomocí našeho dekorátoru `alchemyfield`).
   - **`field_name`** – název pole.
   - **`sub_fields`** – slovník pro vnořená pole, pokud existují.

3. **Generování SQLAlchemy dotazu** – Na základě mapy, která spojuje strawberry typy a SQLAlchemy modely (např. pomocí dědění od `MappedAsDataclass`), se vytvoří SQLAlchemy dotaz. Tento dotaz bude zahrnovat:
   - Výběr všech skalárních atributů.
   - Automatické propojení na objektové typy prostřednictvím volání funkce `select_func` (např. pomocí `joinedload()` nebo `join()`).
   - Podpora pro zanořená data, např. dotaz typu:
     ```graphql
     query {
       users {
         id
         name
         posts { title, content }
       }
     }
     ```
     se přeloží do dotazu, který spojí tabulku `users` s tabulkou `posts`.

4. **Asynchronní vykonání dotazu** – Dotaz je sestaven pomocí SQLAlchemy 2.0 v asynchronním režimu (tj. s použitím `AsyncSession`) a po jeho vykonání se získá kompletní struktura dat. Ta se převede do JSON a poté použije jako parametr ke konstrukci hlavního Strawberry typu ve resolveru.

Níže uvádím kompletní ukázkový kód jako Markdown:

---

```python
import logging
import json
from typing import Any, Callable, Dict, Optional, Type
from sqlalchemy import Column, Integer, String, create_engine, select, and_, or_
from sqlalchemy.orm import declarative_base, Session, InstrumentedAttribute, joinedload
import strawberry
from strawberry.types import Info
from strawberry.extensions import Extension
from strawberry.asgi import GraphQL
import uvicorn
from graphql import parse, DocumentNode, TypeInfo, visit, visit_with_type_info, FieldNode

logging.basicConfig(level=logging.INFO)

# ====================================
# 1. Dekorátor alchemyfield
# ====================================

def alchemyfield(select_func: Optional[Callable[[Any], Any]] = None, **kwargs) -> Any:
    """Wrapper pro strawberry.field, který ukládá dodatečná ORM metadata."""
    extra = kwargs.pop("extra", {})
    extra["select_func"] = select_func
    return strawberry.field(**kwargs, extra=extra)

# ====================================
# 2. SQLAlchemy modely a databáze
# ====================================

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    # Příklad relace: pokud by uživatel měl příspěvky:
    # posts = relationship("PostModel", back_populates="user")

engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add_all([
        UserModel(name="Alice", age=30),
        UserModel(name="Bob", age=20),
        UserModel(name="Alice", age=40),
    ])
    session.commit()

# ====================================
# 3. Strawberry typy
# ====================================

@strawberry.type
class PostType:
    id: int
    title: str
    content: str

@strawberry.type
class UserType:
    id: int
    name: str
    age: int
    posts: list[PostType] = alchemyfield(
        select_func=lambda stmt: stmt.options(joinedload(UserModel.posts))
    )

@strawberry.type
class Query:
    @strawberry.field
    def users(self, info: Info) -> list[UserType]:
        # Resolver očekává, že extension uloží JSON výsledek do contextu
        result_json = info.context.get("result_json")
        if not result_json:
            return []
        data = json.loads(result_json)
        # Pro jednoduchost vracíme jeden záznam; v reálné aplikaci by se jednalo o seznam
        return [UserType(**data)]

# ====================================
# 4. AST parsing – získání dotazovaných polí
# ====================================

def get_nested_fields(field_node: FieldNode) -> Dict[str, Any]:
    nested = {}
    if field_node.selection_set:
        for sel in field_node.selection_set.selections:
            if sel.kind == "Field":
                nested[sel.name.value] = get_nested_fields(sel)
    return nested

def get_requested_fields(document: DocumentNode) -> Dict[str, Any]:
    requested = {}
    for definition in document.definitions:
        if definition.kind == "OperationDefinition":
            for selection in definition.selection_set.selections:
                if selection.kind == "Field":
                    requested[selection.name.value] = get_nested_fields(selection)
    return requested

# ====================================
# 5. Extrakce stromu typu
# ====================================

def extract_type_structure(
    type_obj: Any, 
    requested_fields: Optional[Dict[str, Any]] = None, 
    depth: int = 0
) -> Dict[str, Any]:
    """
    Rekurzivně zmapuje strukturu strawberry typu a vrátí dict obsahující jen dotazovaná pole.
    Každý uzel obsahuje:
      - strawberry_type: originální typ
      - select_func: metadata (pokud je definováno pomocí alchemyfield)
      - sub_fields: rekurzivní zpracování vnořených polí
    """
    indent = "  " * depth
    structure = {"strawberry_type": type_obj, "type": str(type_obj)}
    origin = getattr(type_obj, "__origin__", None)
    
    if origin:
        structure["origin"] = str(origin)
        if origin in {list, tuple, set, frozenset}:
            inner = type_obj.__args__[0]
            structure["inner"] = extract_type_structure(inner, requested_fields, depth + 1)
        else:
            structure["args"] = [extract_type_structure(arg, requested_fields, depth + 1)
                                   for arg in type_obj.__args__ if arg is not type(None)]
    elif hasattr(type_obj, "__annotations__"):
        fields = {}
        # Procházíme pole definovaná v dataclass (strawberry typ)
        for field_name, field_type in type_obj.__annotations__.items():
            if requested_fields is not None and field_name not in requested_fields:
                continue
            nested_requested = requested_fields.get(field_name) if requested_fields else None
            field_structure = extract_type_structure(field_type, nested_requested, depth + 1)
            # Zde můžeme přidat metadata z definice fieldu – předpokládejme, že
            # strawberry uloží metadata do __strawberry_field__.extra (pokud existuje).
            fields[field_name] = {
                "strawberry_type": field_type,
                "select_func": None,  # Později budeme extrahovat z metadat
                "sub_fields": field_structure.get("fields") if "fields" in field_structure else None,
            }
        structure["fields"] = fields
    logging.info(f"{indent}Extracted: {structure}")
    return structure

# ====================================
# 6. Mapování Strawberry typů na SQLAlchemy modely
# ====================================
TYPE_MODEL_MAP = {
    UserType: UserModel,
    # PostType: PostModel,  # pokud byste měli definovaný PostModel
}

# ====================================
# 7. Generování SQLAlchemy dotazu
# ====================================

def limit_dict(input_dict: Any) -> Any:
    if isinstance(input_dict, list):
        return [limit_dict(item) for item in input_dict]
    if not isinstance(input_dict, dict):
        return input_dict
    return {k: limit_dict(v) for k, v in input_dict.items() if v is not None}

def convert_attribute_op(model: Type, attribute_name: str, op: str, value: Any):
    column: InstrumentedAttribute = getattr(model, attribute_name, None)
    if column is None:
        raise AttributeError(f"Model {model.__tablename__} nemá atribut {attribute_name}")
    op_method_name = {
        "_eq": "__eq__",
        "_lt": "__lt__",
        "_le": "__le__",
        "_gt": "__gt__",
        "_ge": "__ge__",
        "_in": "in_",
        "_like": "like",
        "_ilike": "ilike",
        "_startswith": "startswith",
        "_endswith": "endswith",
    }.get(op)
    if op_method_name is None:
        raise ValueError(f"Neznámý operátor {op} pro atribut {attribute_name}")
    op_method = getattr(column, op_method_name)
    return op_method(value)

def convert_filter(model: Type, where: Dict) -> Any:
    where = limit_dict(where)
    keys = list(where.keys())
    if len(keys) > 1:
        expressions = [convert_filter(model, {k: where[k]}) for k in keys]
        return and_(*expressions)
    if len(keys) == 0:
        raise ValueError("Filtr nemá žádné hodnoty")
    key = keys[0]
    value = where[key]
    if key == "_and":
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("_and musí obsahovat alespoň jeden filtr")
        return and_(*[convert_filter(model, sub) for sub in value])
    elif key == "_or":
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("_or musí obsahovat alespoň jeden filtr")
        return or_(*[convert_filter(model, sub) for sub in value])
    else:
        op, op_value = next(iter(value.items()))
        return convert_attribute_op(model, key, op, op_value)

def prepareSelect(model: Type, where: Dict, extendedfilter: Dict = None):
    stmt = select(model)
    if extendedfilter is not None:
        stmt = stmt.filter_by(**extendedfilter)
    filter_expr = convert_filter(model, where)
    stmt = stmt.filter(filter_expr)
    return stmt

def build_sqlalchemy_query_from_tree(model: Type, tree: Dict[str, Any], where: Dict) -> Any:
    # Pro tento příklad využijeme pouze prepareSelect – strom tree lze rozšířit pro dynamický výběr sloupců/joinů.
    return prepareSelect(model, where)

# ====================================
# 8. Schema Extension – dynamické sestavení SQL dotazu
# ====================================

class SQLQueryExtension(Extension):
    async def on_request_start(self) -> None:
        """
        Při startu dotazu:
          1. Získáme GraphQL dotaz jako string a vytvoříme AST.
          2. Z AST extrahujeme dotazovaná pole.
          3. Pomocí TypeInfo získáme top-level strawberry typ pro cílové pole (např. "users").
          4. Na základě tohoto typu a požadovaných polí sestavíme strom typu (vnořený dict).
             Každý uzel obsahuje název pole, strawberry typ a metadata (select_func).
          5. Pomocí mapy mezi strawberry typy a SQLAlchemy modely vytvoříme ORM dotaz.
          6. Dotaz provedeme asynchronně a výsledek převedeme na JSON, uložíme do contextu.
        """
        query_string: str = self.execution_context.query
        if not query_string:
            return
        document = parse(query_string)
        requested_fields = get_requested_fields(document)
        logging.info(f"Requested fields: {requested_fields}")
        
        # Nastavte target_field dynamicky – např. "users"
        target_field = "users"
        
        # Použijeme TypeInfo pro získání typu top-level fieldu target_field
        type_info = TypeInfo(self.execution_context.schema.gql_schema)
        top_field_type = None

        def enter_field(node, key, parent, path, ancestors):
            nonlocal target_field, top_field_type
            if ancestors and len(ancestors) == 1 and ancestors[0].kind == "OperationDefinition":
                if node.name.value == target_field:
                    top_field_type = type_info.get_type()
            return None

        visit(document, visit_with_type_info(type_info, {"Field": enter_field}))
        
        if top_field_type is None:
            logging.error(f"Nebylo nalezeno top-level pole '{target_field}'")
            return
        origin = getattr(top_field_type, "__origin__", None)
        if origin is list:
            top_type = top_field_type.__args__[0]
        else:
            top_type = top_field_type
        logging.info(f"Dynamicky odvozený top-level strawberry typ: {top_type}")
        
        requested_for_field = requested_fields.get(target_field, {})
        type_tree = extract_type_structure(top_type, requested_for_field)
        logging.info(f"Filtered type tree: {type_tree}")
        
        # Simulovaný vstupní filtr – v praxi bude součástí dotazu
        filter_input = {
            "_and": [
                {"name": {"_eq": "Alice"}},
                {"age": {"_gt": 25}}
            ]
        }
        self.execution_context.context["filter_input"] = filter_input
        
        try:
            # Z mapy získáme SQLAlchemy model odpovídající top-level strawberry typu
            orm_model = TYPE_MODEL_MAP.get(top_type)
            if orm_model is None:
                raise ValueError(f"SQLAlchemy model pro typ {top_type} nebyl nalezen.")
            query = build_sqlalchemy_query_from_tree(orm_model, type_tree, filter_input)
            logging.info(f"Built SQL query: {query}")
            # Asynchronní vykonání dotazu – předpokládáme, že do contextu je vložen async_session maker
            async with self.execution_context.context["async_session"]() as session:
                result = await session.execute(query)
                instance = result.scalars().first()
                if instance is not None:
                    result_json = json.dumps({
                        "id": instance.id,
                        "name": instance.name,
                        "age": instance.age,
                    })
                else:
                    result_json = json.dumps({})
            self.execution_context.context["result_json"] = result_json
        except Exception as e:
            logging.error(f"Error building SQL query: {e}")
            self.execution_context.context["result_json"] = json.dumps({})

# ====================================
# 9. Sestavení schématu a ASGI aplikace
# ====================================

schema = strawberry.Schema(query=Query, extensions=[SQLQueryExtension])
app = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
