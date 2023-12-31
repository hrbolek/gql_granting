from typing import List, Union, Optional, Annotated
import strawberry 
import strawberry as strawberryA
#from .AcProgramGQLModel import AcProgramGQLModel
from contextlib import asynccontextmanager
from gql_granting.GraphResolvers import resolveProgramForGroup, resolveJSONForProgram
from .AcClassificationGQLModel import AcClassificationGQLModel
from uuid import UUID

AcProgramGQLModel= Annotated["AcProgramGQLModel",strawberryA.lazy(".AcProgramGQLModel")]

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return GroupGQLModel(id=id)
    async def program(
        self, info: strawberryA.types.Info
    ) -> Union["AcProgramGQLModel", None]:
        async with withInfo(info) as session:
            result = await resolveProgramForGroup(session, id)
            return result


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: UUID = strawberryA.federation.field(external=True)
    @classmethod
    async def resolve_reference(cls, id:UUID):
        return UserGQLModel(id=id)

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,self.id)
#         return result


    @strawberryA.field(description="""List of programs which the user is studying""")
    async def study_programs(self, info: strawberryA.types.Info) -> List['AcProgramGQLModel']:
         
        loader = getLoaders(info).programstudents
        result = await loader.filter_by(student_id=self.id)       
        return result
    
    @strawberryA.field(description="""List of programs which the user is studying""")
    async def classifications(self, info: strawberryA.types.Info) -> List['AcClassificationGQLModel']:
        loader = getLoaders(info).classifications
        result = await loader.filter_by(user_id=self.id)       
        return result