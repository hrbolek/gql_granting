from src.GraphTypeDefinitions import schema

schema.extensions = []
MD_FILE_PATH = "./graphql_schema.md"


def extract_type_name(field_type):
    """Vrátí správný název typu včetně podpory List[], NonNull! a dalších.
    Returns the correct type name, including support for List[], NonNull!, and more."""

    while field_type:
        kind = field_type.get("kind", "")
        name = field_type.get("name")

        if kind == "LIST" and field_type.get("ofType"):
            return f"List[{extract_type_name(field_type['ofType'])}]"

        if kind == "NON_NULL" and field_type.get("ofType"):
            return f"{extract_type_name(field_type['ofType'])}!"

        if name:
            return name  # Jakmile najdeme platný název, vrátíme ho

        field_type = field_type.get("ofType")  # Posuneme se hlouběji

    return "Unknown"

def generate_markdown_from_schema():   
    """Generuje Markdown dokumentaci z introspektovaného GraphQL schématu.
    Generates Markdown documentation from the introspected GraphQL schema."""

    INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    types {
      name
      description
      fields {
        name
        description
        type {
          name
          kind
          ofType {
            name
            kind
            ofType {
              name
              kind
              ofType {
                name
                kind
                ofType {
                  name
                  kind
                }
              }
            }
          }
        }
      }
    }
  }
}
    """    

    # Spustíme introspekční dotaz přímo nad objektem `schema`
    result = schema.execute_sync(INTROSPECTION_QUERY)
    
    if result.errors:
        raise Exception(f"GraphQL introspection failed: {result.errors}")

    schema_data = result.data

    markdown_content = "# GraphQL API Documentation\n\n"

    for gql_type in schema_data["__schema"]["types"]:
        if gql_type["name"].startswith("__"):  # Přeskakujeme interní GraphQL typy
            continue

        description = gql_type["description"] or "No description available."
        markdown_content += f"## {gql_type['name']}\n\n"
        markdown_content += description.replace("\n", "  \n") + "\n\n"  # Zachování zalomení řádků

        if gql_type.get("fields"):
            markdown_content += "### Fields:\n\n"
            for field in gql_type["fields"]:
                field_name = field["name"]
                field_desc = (field["description"] or "No description available.").replace("\n", "  \n")
                field_type = extract_type_name(field["type"])
                
                markdown_content += f"- **{field_name}** (`{field_type}`): \n\n    {field_desc}\n"

        markdown_content += "\n---\n"

    return markdown_content

from graphql import get_introspection_query
introspection_query = get_introspection_query(descriptions=True)

def format_type(type_ref):
    """
    Rekurzivně převede GraphQL type reference na textovou reprezentaci.
    Např. NON_NULL => "Typ!" a LIST => "[Typ]".
    """
    if type_ref is None:
        return ""
    kind = type_ref.get("kind")
    if kind == "NON_NULL":
        return f"{format_type(type_ref.get('ofType'))}!"
    elif kind == "LIST":
        return f"[{format_type(type_ref.get('ofType'))}]"
    else:
        return type_ref.get("name") or ""

def markdown_for_field(field):
    """
    Vytvoří Markdown řádek pro pole (field) v objektu nebo query/mutation.
    Zahrnuje název, typ a případně popis a argumenty.
    """
    s = f"- **{field['name']}**: `{format_type(field['type'])}`"
    if field.get("description"):
        s += f" – {field['description']}"
    if field.get("args"):
        if len(field["args"]) > 0:
            s += "\n  - **Arguments:**"
            for arg in field["args"]:
                s += f"\n    - **{arg['name']}**: `{format_type(arg['type'])}`"
                if arg.get("description"):
                    s += f" – {arg['description']}"
    return s

def markdown_for_input_field(field):
    """
    Vytvoří Markdown řádek pro vstupní pole (input field).
    """
    s = f"- **{field['name']}**: `{format_type(field['type'])}`"
    if field.get("description"):
        s += f" – {field['description']}"
    return s

def markdown_for_object_type(type_obj):
    """
    Vygeneruje Markdown popis pro objektový typ (fields, popis).
    """
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    if type_obj.get("fields"):
        s += "Fields:\n"
        for field in type_obj["fields"]:
            s += markdown_for_field(field) + "\n"
        s += "\n"
    return s

def markdown_for_input_object_type(type_obj):
    """
    Vygeneruje Markdown popis pro vstupní objekt.
    """
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    if type_obj.get("inputFields"):
        s += "Input Fields:\n"
        for field in type_obj["inputFields"]:
            s += markdown_for_input_field(field) + "\n"
        s += "\n"
    return s

def markdown_for_scalar_type(type_obj):
    """
    Vygeneruje Markdown popis pro skalární typ.
    """
    s = f"#### {type_obj['name']}\n\n"
    if type_obj.get("description"):
        s += f"{type_obj['description']}\n\n"
    return s


# --- Hlavní funkce, která provede introspekci a vygeneruje Markdown dokumentaci ---

def generate_markdown_from_schema2():
    # Provedeme introspekci schématu
    # introspection_query = get_introspection_query(descriptions=True)
    result = schema.execute_sync(introspection_query)
    if result.errors:
        print("Chyby při introspekci:", result.errors)
        return

    schema_data = result.data["__schema"]
    types = schema_data["types"]

    # Zjistíme názvy query a mutation typů
    query_type_name = schema_data["queryType"]["name"] if schema_data.get("queryType") else None
    mutation_type_name = schema_data["mutationType"]["name"] if schema_data.get("mutationType") else None

    query_type = None
    mutation_type = None
    scalars = []
    inputs = []
    objects = []

    # Rozřadíme typy do kategorií (ignorujeme interní typy začínající "__")
    for t in types:
        if t["name"].startswith("__"):
            continue
        if t["name"] == query_type_name:
            query_type = t
        elif t["name"] == mutation_type_name:
            mutation_type = t
        elif t["kind"] == "SCALAR":
            scalars.append(t)
        elif t["kind"] == "INPUT_OBJECT":
            inputs.append(t)
        elif t["kind"] == "OBJECT":
            objects.append(t)

    markdown = "# GraphQL Schema Documentation\n\n"

    # Sekce Query a Mutation
    markdown += "## Query a Mutation\n\n"
    if query_type:
        markdown += f"### Query: {query_type['name']}\n\n"
        if query_type.get("description"):
            markdown += f"{query_type['description']}\n\n"
        if query_type.get("fields"):
            markdown += "Fields:\n"
            for field in query_type["fields"]:
                markdown += markdown_for_field(field) + "\n"
        markdown += "\n"

    if mutation_type:
        markdown += f"### Mutation: {mutation_type['name']}\n\n"
        if mutation_type.get("description"):
            markdown += f"{mutation_type['description']}\n\n"
        if mutation_type.get("fields"):
            markdown += "Fields:\n"
            for field in mutation_type["fields"]:
                markdown += markdown_for_field(field) + "\n"
        markdown += "\n"

    # Sekce Skaláry
    markdown += "## Skaláry\n\n"
    for scalar in scalars:
        markdown += markdown_for_scalar_type(scalar)

    # Sekce Vstupní typy (inputs)
    markdown += "## Vstupní typy\n\n"
    for input_obj in inputs:
        markdown += markdown_for_input_object_type(input_obj)

    # Sekce Regulérní typy (objects)
    markdown += "## Regulérní typy\n\n"
    for obj in objects:
        # Vynecháme již zpracované query a mutation typy
        if obj["name"] in [query_type_name, mutation_type_name]:
            continue
        markdown += markdown_for_object_type(obj)
    return markdown


markdown_content = generate_markdown_from_schema()
with open(MD_FILE_PATH, "w", encoding="utf-8") as md_file:
    md_file.write(markdown_content)

markdown_content = generate_markdown_from_schema2()
with open(MD_FILE_PATH + ".md", "w", encoding="utf-8") as md_file:
    md_file.write(markdown_content)