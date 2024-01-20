from typing import List
from fastapi import FastAPI
import os
import strawberry
from strawberry.fastapi import GraphQLRouter


import logging
import logging.handlers
import socket
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')
SYSLOGHOST = os.getenv("SYSLOGHOST", None)
if SYSLOGHOST is not None:
    [address, strport, *_] = SYSLOGHOST.split(':')
    assert len(_) == 0, f"SYSLOGHOST {SYSLOGHOST} has unexpected structure, try `localhost:514` or similar (514 is UDP port)"
    port = int(strport)
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(address, port), socktype=socket.SOCK_DGRAM)
    #handler = logging.handlers.SocketHandler('10.10.11.11', 611)
    my_logger.addHandler(handler)



## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from gql_granting.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


from gql_granting.DBFeeder import initDB


@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """
    print(f'starting engine for "{connectionString}"')

    import os
    makeDrop = os.environ.get("DEMO", "") == "True"
    makeDrop = True
    result = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )

    print(f"initializing system structures")

    ###########################################################################################################################
    #
    # zde definujte do funkce asyncio.gather
    # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
    await initDB(result)
    #
    #
    ###########################################################################################################################
    print(f"all done")
    return result


from strawberry.asgi import GraphQL

from gql_granting.Dataloaders import createLoaders

class MyGraphQL(GraphQL):
    """Rozsirena trida zabezpecujici praci se session"""

    async def __call__(self, scope, receive, send):
        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        async with asyncSessionMaker() as session:
            self._session = session
            self._user = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
            return await GraphQL.__call__(self, scope, receive, send)

    async def get_context(self, request, response):
        parentResult = await GraphQL.get_context(self, request, response)
        asyncSessionMaker = await RunOnceAndReturnSessionMaker()
        return {
            **parentResult,
            "session": self._session,
            "asyncSessionMaker": asyncSessionMaker,
            "user": self._user,
            # "all": await createLoaders_3(asyncSessionMaker)
            # "all": createLoaders(asyncSessionMaker),
            "loaders": createLoaders(asyncSessionMaker)
        }

from gql_granting.GraphTypeDefinitions import schema

## ASGI app, kterou "moutneme"
graphql_app = MyGraphQL(schema, graphql_ide="graphiql", allow_queries_via_get=True)

app = FastAPI()
app.mount("/gql", graphql_app)


@app.on_event("startup")
async def startup_event():
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    return None


print("All initialization is done")

# @app.get('/hello')
# def hello():
#    return {'hello': 'world'}

###########################################################################################################################
#
# pokud jste pripraveni testovat GQL funkcionalitu, rozsirte apollo/server.js
#
###########################################################################################################################


def envAssertDefined(name, default=None):
    result = os.getenv(name, None)
    assert result is not None, f"{name} environment variable must be explicitly defined"
    return result

DEMO = envAssertDefined("DEMO", None)
GQLUG_ENDPOINT_URL = envAssertDefined("GQLUG_ENDPOINT_URL", None)
JWTPUBLICKEYURL = envAssertDefined("JWTPUBLICKEYURL", None)
JWTRESOLVEUSERPATHURL = envAssertDefined("JWTRESOLVEUSERPATHURL", None)

assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")
else:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING DEPLOYMENT                               #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING DEPLOYMENT                               #")
    logging.info("#                                                  #")
    logging.info("####################################################")    

logging.info(f"DEMO = {DEMO}")
logging.info(f"SYSLOGHOST = {SYSLOGHOST}")
logging.info(f"GQLUG_ENDPOINT_URL = {GQLUG_ENDPOINT_URL}")
logging.info(f"JWTPUBLICKEYURL = {JWTPUBLICKEYURL}")
logging.info(f"JWTRESOLVEUSERPATHURL = {JWTRESOLVEUSERPATHURL}")