import pytest
import logging
import uuid
import sqlalchemy

def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Env_GQLUG_ENDPOINT_URL_8124):
        
        def testResult(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None, f"Error during byId Execution {errors}"
            
            respdata = resp.get("data", None)
            assert respdata is not None, f"Empty response, check loader and datatable"
            
            respdata = respdata["result"]
            assert respdata is not None, f"{queryEndpoint} returns None {resp} as result of query for {query} with {variable_values}"

            for att in attributeNames:
                assert respdata[att] == f'{datarow[att]}'

        schemaExecutor = ClientExecutorDemo
        clientExecutor = SchemaExecutorDemo

        data = DemoData
        table = data.get(tableName, None)
        assert table is not None, f"{tableName} not found in demodata"
        assert len(table) > 0, f"{tableName} is empty"
        datarow = table[0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"result: {queryEndpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{datarow["id"]}'}
        
        # append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
        logging.debug(f"query for {query} with {variable_values}")

        # resp = await schemaExecutor(query, variable_values)
        # testResult(resp)
        resp = await clientExecutor(query, variable_values)
        testResult(resp)

    return result_test

def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo):

        def testResult(resp):
            errors = resp.get("errors", None)
            assert errors is None
            respdata = resp.get("data", None)
            assert respdata is not None

            respdata = respdata.get(queryEndpoint, None)
            assert respdata is not None
            datarows = data[tableName]           

            for rowa, rowb in zip(respdata, datarows):
                for att in attributeNames:
                    assert rowa[att] == f'{rowb[att]}', f"attribute `{att}` not equal {rowa[att]} != {rowb[att]}" 

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        data = DemoData

        content = "{" + ", ".join(attributeNames) + "}"
        query = "query{" f"{queryEndpoint}" f"{content}" "}"

        # append(queryname=f"{queryEndpoint}_{tableName}", query=query)

        resp = await schemaExecutor(query)
        testResult(resp)
        resp = await clientExecutor(query)
        testResult(resp)
        
    return result_test

def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):

        def testResult(resp):
            print(resp)
            errors = resp.get("errors", None)
            assert errors is None, errors
            respdata = resp.get("data", None)
            assert respdata is not None

            logging.info(respdata)
            respdata = respdata.get('_entities', None)
            assert respdata is not None

            assert len(respdata) == 1, f"got no data, is defined proper loader? test at proper table? ({tableName})"
            respdata = respdata[0]
            assert respdata is not None, f"Seems database table {tableName} is not initialized for test (conftest.py / Demodata?), also test loader"
            assert respdata['id'] == rowid, f"got id {respdata['id']} != {rowid}"

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        content = "{" + ", ".join(attributeNames) + "}"

        data = DemoData
        table = data[tableName]
        for row in table:
            rowid = f"{row['id']}"

            statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName} WHERE id=:id").bindparams(id=row['id'])
            statement2 = sqlalchemy.text(f"SELECT id FROM {tableName}")
            #statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
            # print("statement", statement, flush=True)
            async with SQLite() as session:
                rows = await session.execute(statement)
                row = rows.first()
                if row is None:
                    rows = await session.execute(statement2)
                    ids = list(rows.scalars())

                    logging.info(f"table {tableName} has rows with ids {ids}. Id {row['id']} has been not found.")
                    assert row is not None, f"row with id={row['id']} not found in table {tableName}"

            # query = (
            #     'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
            #     ' }])' +
            #     '{' +
            #     f'...on {gqltype}' + content +
            #     '}' + 
            #     '}')

            # variable_values = {"id": rowid}

            query = ("query($rep: [_Any!]!)" + 
                "{" +
                "_entities(representations: $rep)" +
                "{"+
                f"    ...on {gqltype} {content}"+
                "}"+
                "}"
            )
            
            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{rowid}"}]}

            logging.info(f"query representations {query} with {variable_values}")
            # resp = await clientExecutor(query, {**variable_values})
            # testResult(resp)
            resp = await schemaExecutor(query, {**variable_values})
            testResult(resp)

        # append(queryname=f"{gqltype}_representation", query=query)

    return result_test

def createFrontendQuery(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):    
        logging.debug("createFrontendQuery")
        # async_session_maker = await prepare_in_memory_sqllite()
        # await prepare_demodata(async_session_maker)
        # context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query", query=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query, 
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query, 
        #     variable_values=variables, 
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        logging.info(f"query for \n{query} with \n{variables} got response: \n{respdata}")
        for a in asserts:
            a(respdata)
    return test_frontend_query


def createUpdateQuery(query="{}", variables={}, tableName=""):
    @pytest.mark.asyncio
    async def test_update(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):
        logging.debug("test_update")
        assert variables.get("id", None) is not None, "variables has not id"
        variables["id"] = uuid.UUID(f"{variables['id']}")
        assert "$lastchange: DateTime!" in query, "query must have parameter $lastchange: DateTime!"
        assert "lastchange: $lastchange" in query, "query must use lastchange: $lastchange"
        assert tableName != "", "missing table name"

        async_session_maker = SQLite

        print("variables['id']", variables, flush=True)
        statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName} WHERE id=:id").bindparams(id=variables['id'])
        #statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
        print("statement", statement, flush=True)
        async with async_session_maker() as session:
            rows = await session.execute(statement)
            row = rows.first()
            
            print("row", row)
            id = row[0]
            lastchange = row[1]

            print(id, lastchange)

        variables["lastchange"] = lastchange
        variables["id"] = f'{variables["id"]}'
        context_value = Context
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query_{tableName}", mutation=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query, 
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query, 
        #     variable_values=variables, 
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        assert respdata is not None, "GQL response is empty"
        print("respdata", respdata)
        keys = list(respdata.keys())
        assert len(keys) == 1, "expected update test has one result"
        key = keys[0]
        result = respdata.get(key, None)
        assert result is not None, f"{key} is None (test update) with {query}"
        entity = None
        for key, value in result.items():
            print(key, value, type(value))
            if isinstance(value, dict):
                entity = value
                break
        assert entity is not None, f"expected entity in response to {query}"

        for key, value in entity.items():
            if key in ["id", "lastchange"]:
                continue
            print("attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}")
            assert value == variables[key], f"test on update failed {value} != {variables[key]}"

        

    return test_update




def unwrap_type(type_):
    """
    Unwraps NON_NULL and LIST wrappers to get the base type
    """
    t = type_
    while t["kind"] in ('NON_NULL', 'LIST'):
        t = t["ofType"]
    return t


def get_read_scalar_value(schema: dict) -> dict:
    """
    Map of single‑ID query return types.

    Given a GraphQL introspection schema (as nested dictionaries/lists),
    returns a dict mapping each OBJECT return type name to the
    corresponding query field name that takes a single NON_NULL id arg.
    """
    result = {}

    # Find the Query type definition
    query_type_name = schema["queryType"]["name"]
    query_type = next(
        (t for t in schema["types"] if t["name"] == query_type_name),
        None
    )
    if not query_type:
        return result

    # Inspect each field on the Query type
    for field in query_type.get("fields", []):
        args = field.get("args", [])
        # Must have exactly one argument named "id" which is NON_NULL
        if (
            len(args) == 1
            and args[0]["name"] == "id"
            and args[0]["type"]["kind"] == "NON_NULL"
        ):
            ret_type = field.get("type", {})
            # If the return type is an OBJECT, record it
            if ret_type.get("kind") == "OBJECT":
                obj_name = ret_type["name"]
                result[obj_name] = field["name"]

    return result

def get_read_vector_value(schema: dict) -> dict:
    """
    Map of nonNull list of nonNull object queries:
    vrací slovník {Typ: názevQueryFieldu}
    """
    result = {}
    # najdi Query typ
    qtype = next((t for t in schema["types"]
                  if t["name"] == schema["queryType"]["name"]), None)
    if not qtype:
        return result

    for f in qtype.get("fields", []):
        t = f["type"]
        if t.get("kind") == "NON_NULL":
            list_t = t.get("ofType")
            if list_t and list_t.get("kind") == "LIST":
                mem = list_t.get("ofType")
                if mem and mem.get("kind") == "NON_NULL":
                    base = mem.get("ofType")
                    if base and base.get("kind") == "OBJECT":
                        result[base["name"]] = f["name"]
    return result


def get_insert_mutations(schema: dict) -> dict:
    """
    Map of insert mutations:
    hledá mutace s jediným NON_NULL argumentem INPUT_OBJECT
    bez povinného fieldu lastchange,
    vrací slovník {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp:
                    names = [i["name"] for i in inp.get("inputFields", [])]
                    # bez lastchange
                    if "lastchange" not in names:
                        ret = unwrap_type(f["type"])
                        if ret and ret.get("kind") == "UNION":
                            union_def = next((t for t in schema["types"]
                                              if t["name"] == ret["name"]), None)
                            for pt in union_def.get("possibleTypes", []):
                                if pt["kind"] == "OBJECT" and "Error" not in pt["name"]:
                                    result[pt["name"]] = f["name"]
    return result


def get_update_mutations(schema: dict) -> dict:
    """
    Map of update mutations:
    hledá mutace s jediným NON_NULL INPUT_OBJECT argumentem,
    který má >2 inputFields včetně povinných id & lastchange,
    vrací {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp and len(inp.get("inputFields", [])) > 2:
                    req = [i["name"] for i in inp["inputFields"] if i["type"]["kind"] == "NON_NULL"]
                    if "id" in req and "lastchange" in req:
                        ret = unwrap_type(f["type"])
                        if ret and ret.get("kind") == "UNION":
                            union_def = next((t for t in schema["types"]
                                              if t["name"] == ret["name"]), None)
                            for pt in union_def.get("possibleTypes", []):
                                if pt["kind"] == "OBJECT" and "Error" not in pt["name"]:
                                    result[pt["name"]] = f["name"]
    return result


def get_delete_mutations(schema: dict) -> dict:
    """
    Map of delete mutations:
    hledá mutace s jediným NON_NULL INPUT_OBJECT argumentem,
    jehož inputFields obsahují právě id & lastchange,
    a return OBJECT, kde field 'Entity' ukáže původní typ,
    vrací {Typ: názevMutace}
    """
    result = {}
    mtype = next((t for t in schema["types"]
                  if t["name"] == schema["mutationType"]["name"]), None)
    if not mtype:
        return result

    for f in mtype.get("fields", []):
        args = f.get("args", [])
        if len(args) == 1 and args[0]["type"]["kind"] == "NON_NULL":
            arg_def = unwrap_type(args[0]["type"])
            if arg_def and arg_def.get("kind") == "INPUT_OBJECT":
                inp = next((t for t in schema["types"] if t["name"] == arg_def["name"]), None)
                if inp:
                    req = [i["name"] for i in inp.get("inputFields", [])
                           if i["type"]["kind"] == "NON_NULL"]
                    if set(req) == {"id", "lastchange"}:
                        # rozbal return typ
                        ret = f["type"]
                        if ret.get("kind") == "NON_NULL":
                            ret = ret["ofType"]
                        if ret.get("kind") == "OBJECT":
                            ret_def = next((t for t in schema["types"]
                                            if t["name"] == ret["name"]), None)
                            if ret_def:
                                entity_field = next((fl for fl in ret_def["fields"]
                                                     if fl["name"] == "Entity"), None)
                                if entity_field:
                                    entity_type = unwrap_type(entity_field["type"])["name"]
                                    result[entity_type] = f["name"]
    return result


def get_cruds(schema: dict) -> dict:
    """
    Kombinuje všechny čtyři předchozí mapy a vrací
    slovník {Typ: {read, readp, insert?, update?, delete?}}
    pouze pro typy, které podporují read & readp.
    """
    single = get_read_scalar_value(schema)
    vector = get_read_vector_value(schema)
    ins = get_insert_mutations(schema)
    upd = get_update_mutations(schema)
    dele = get_delete_mutations(schema)

    cruds = {}
    for t, read_name in single.items():
        if t in vector:
            cruds[t] = {
                "read": read_name,
                "readp": vector[t],
                **({"insert": ins[t]} if t in ins else {}),
                **({"update": upd[t]} if t in upd else {}),
                **({"delete": dele[t]} if t in dele else {}),
            }
    return cruds


introspectionQuery = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      description
      kind
      fields {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
      inputFields {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
      possibleTypes {
        name
        kind
      }
    }
  }
}"""

def build_selection_optional(schema: dict, field_type: dict) -> str:
    """
    Builds a selection set by iterating over fields of the given object type.
    Includes only fields that have no args or only optional args.
    For fields returning OBJECT or LIST of OBJECT, nests them with `{ __typename id }`.
    """
    base = unwrap_type(field_type)
    if base.get("kind") != "OBJECT":
        return ""
    # find type definition
    type_def = next((t for t in schema["types"] if t.get("name") == base.get("name")), None)
    if not type_def or not type_def.get("fields"):
        return ""

    parts = []
    for f in type_def["fields"]:
        name = f.get("name")
        if name.startswith("__"):
            continue
        args = f.get("args", [])
        # only fields without args or only optional args
        if args and any(arg["type"]["kind"] == "NON_NULL" for arg in args):
            continue
        ret_base = unwrap_type(f.get("type"))
        if ret_base.get("kind") == "OBJECT":
            parts.append(f"{name} {{ __typename id }}")
        else:
            parts.append(name)
    if not parts:
        return ""
    joined = "\n  ".join(parts)
    return f"{{ {joined} }}"


def build_selection(schema: dict, field_type: dict) -> str:
    """
    Recursively builds selection set based on kind of field_type.
    """
    if not field_type or not field_type.get("kind"):
        return ""
    kind = field_type["kind"]
    if kind == "SCALAR":
        return ""
    if kind == "OBJECT":
        return build_selection_optional(schema, field_type)
    if kind == "LIST":
        return build_selection(schema, field_type.get("ofType"))
    if kind == "NON_NULL":
        return build_selection(schema, field_type.get("ofType"))
    if kind == "UNION":
        # fallback: only __typename
        return "{ __typename }"
    # unknown: return empty
    return ""


def print_type(type_ref: dict) -> str:
    """
    Prints GraphQL type signature, handling NON_NULL and LIST.
    """
    if not type_ref:
        return ""
    kind = type_ref.get("kind")
    if kind == "NON_NULL":
        return f"{print_type(type_ref.get('ofType'))}!"
    if kind == "LIST":
        return f"[{print_type(type_ref.get('ofType'))}]"
    # SCALAR or OBJECT etc.
    return type_ref.get("name", "")


def build_input_type_params(schema: dict, input_type_name: str) -> str:
    """
    Builds parameter definitions string for given INPUT_OBJECT type.
    Outputs GraphQL variable signature, e.g.:
      ($field1: Type1!, $field2: Type2)
    """
    inp_def = next((t for t in schema["types"]
                    if t.get("name") == input_type_name and t.get("kind") == "INPUT_OBJECT"), None)
    if not inp_def or not inp_def.get("inputFields"):
        return ""
    params = []
    for field in inp_def["inputFields"]:
        raw = field.get("type")
        if raw.get("kind") == "NON_NULL":
            type_str = f"{print_type(raw.get('ofType'))}!"
        else:
            type_str = print_type(raw)
        params.append(f"${field['name']}: {type_str}")
    if not params:
        return ""
    joined = ",\n   ".join(params)
    return f"(\n   {joined}\n)"


def build_expanded_mutation(schema: dict, mutation_name: str) -> str:
    """
    Builds complete GraphQL mutation string for given mutation.
    Uses expanded individual fields as variables based on input type.
    """
    mtype = next((t for t in schema["types"] if t.get("name") == schema["mutationType"]["name"]), None)
    if not mtype:
        return ""
    field = next((f for f in mtype.get("fields", []) if f.get("name") == mutation_name), None)
    if not field or len(field.get("args", [])) != 1:
        return ""
    arg = field["args"][0]
    input_name = unwrap_type(arg.get("type")).get("name")
    param_defs = build_input_type_params(schema, input_name)
    # build call args
    inp_def = next((t for t in schema["types"] if t.get("name") == input_name), {})
    inputs = inp_def.get("inputFields", [])
    call_args = ",\n   ".join(f"{f['name']}: ${f['name']}" for f in inputs)
    # build selection
    ret_base = unwrap_type(field.get("type"))
    selection = ""
    if ret_base.get("kind") == "UNION":
        union_def = next((t for t in schema["types"] if t.get("name") == ret_base.get("name")), {})
        parts = []
        for pt in union_def.get("possibleTypes", []):
            if pt.get("kind") == "OBJECT" and "Error" not in pt.get("name", ""):
                sel = build_selection(schema, {"kind": "OBJECT", "name": pt.get("name")})
                parts.append(f"... on {pt['name']} {sel}")
        joined = "\n   ".join(parts)
        selection = f" {{\n   __typename\n   {joined}\n }}"
    elif ret_base.get("kind") == "OBJECT":
        sel = build_selection(schema, ret_base)
        selection = f" {sel}" if sel else ""
    return f"mutation {param_defs} {{\n  {mutation_name}({arg['name']}: {{\n   {call_args}\n  }}){selection}\n}}"


def build_query_page(schema: dict, operation_name: str) -> str:
    """
    Builds a readPage query for given type.
    """
    query_type_name = schema["queryType"]["name"]
    query_type = next((t for t in schema["types"] if t["name"] == query_type_name), None)
    if not query_type:
        return None
    field_def = next((f for f in query_type.get("fields", []) if f["name"] == operation_name), None)
    if not field_def:
        return None
    field_result_type = unwrap_type(field_def.get("type"))
    if field_result_type.get("kind") != "LIST":
        return None
    list_type = field_result_type.get("ofType")
    if list_type.get("kind") != "NON_NULL":
        return None
    type_def = list_type.get("ofType")
    if type_def.get("kind") != "OBJECT":
        return None
    # find type definition
    type_def = next((t for t in schema["types"] if t["name"] == type_def.get("name")), None)
    if not type_def:
        return None
    sel = build_selection(schema, type_def)
    return f"query {operation_name} {{ {operation_name}{sel} }}"


def build_query_scalar(schema: dict, operation_name: str) -> str:
    """
    Builds a read(id) query for given type.
    """
    query_type_name = schema["queryType"]["name"]
    query_type = next((t for t in schema["types"] if t["name"] == query_type_name), None)
    if not query_type:
        return None
    field_def = next((f for f in query_type.get("fields", []) if f["name"] == operation_name), None)
    if not field_def:
        return None
    field_result_type = unwrap_type(field_def.get("type"))
    if field_result_type.get("kind") != "OBJECT":
        return None
    # find type definition
    type_def = next((t for t in schema["types"] if t["name"] == field_result_type.get("name")), None)
    if not type_def:
        return None
    # find field definition
    
    sel = build_selection(schema, type_def)
    return f"query {operation_name}Read($id: UUID!) {{ {operation_name}(id: $id){sel} }}"

async def test_page(schema, operation, executor):
    query = build_query_page(schema, operation)
    assert query is not None, f"Query for {operation} not found in schema"
    variable_values = {}
    result = await executor(query=query, variable_values=variable_values)
    errors = result.get("errors", None)
    assert errors is None, f"Error during page execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert len(data) > 0, f"Empty response, check loader and datatable"
    return data[0]

async def test_scalar(schema, operation, executor):
    entity = await test_page(schema, operation, executor)
    query = build_query_scalar(schema, operation)
    assert query is not None, f"Query for {operation} not found in schema"
    variable_values = {**entity}
    result = await executor(query=query, variable_values=variable_values)
    errors = result.get("errors", None)
    assert errors is None, f"Error during scalar execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert data.get("id") == variable_values["id"], f"ID mismatch, expected {variable_values['id']} but got {data.get('id')}"

async def test_insert(schema, operation, executor):
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"

    entity = await test_page(schema, operation, executor)
    variable_values = {**entity}
    # remove id and lastchange
    variable_values.pop("id", None)
    variable_values.pop("lastchange", None)
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during insert execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert "Error" not in data.get("__typename", ""), f"{operation} returned {data}"
    return data

async def test_update(schema, operation, executor):
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"
    
    # get entity for update
    entity = await test_insert(schema, operation, executor)
    variable_values = {**entity}
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during update execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is not None, f"Empty response, check loader and datatable"
    assert "Error" not in data.get("__typename", ""), f"{operation} returned {data}"
    return data

async def test_delete(schema, operation, executor):
    query = build_expanded_mutation(schema, operation)
    assert query is not None, f"Mutation for {operation} not found in schema"

    entity = await test_insert(schema, operation, executor)
    variable_values = {**entity}
    result = await executor(query=query, variable_values=variable_values)

    errors = result.get("errors", None)
    assert errors is None, f"Error during delete execution {errors}"
    data = result.get("data", None)
    assert data is not None, f"Empty response, check loader and datatable"
    data = data.get(operation, None)
    assert data is None, f"Expected empty response after delete, got {data}"
    return data

def createTests(schema):
    import strawberry
    s : strawberry.federation.Schema = schema
    introspection = s.execute_sync(introspectionQuery)
    __schema = introspection.data["__schema"]
    cruds = get_cruds(__schema)

    def create_particular_test(schema, operation, executor):
        @pytest.mark.asyncio
        async def test_func(Executor):
            executor = Executor
            if operation == "readp":
                return await test_page(schema, operation, executor)
            elif operation == "read":
                return await test_scalar(schema, operation, executor)
            elif operation == "insert":
                return await test_insert(schema, operation, executor)
            elif operation == "update":
                return await test_update(schema, operation, executor)
            elif operation == "delete":
                return await test_delete(schema, operation, executor)
            else:
                raise ValueError(f"Operation {operation} not found in schema")
        return test_func
    
    for typename, ops in cruds.items():
        for optype, opname in ops.items():
            test = create_particular_test(schema, typename, opname)
            test.__name__ = f"test_{optype}_{typename}"
            globals()[f"test_{optype}_{typename}"] = test
        
        pass


def createByIdTest(typeName):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Env_GQLUG_ENDPOINT_URL_8124):
        #do something
        return
    return result_test
        