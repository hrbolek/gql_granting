import strawberry
import uuid
import typing
import datetime
import logging
import asyncio
from uuid import UUID
from typing import Optional, List, Union, Annotated

from ..utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

#UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".granting")]

@strawberry.federation.type(keys=["id"], description="Study program editor")
class AcProgramEditorGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programs
        return loader

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    # change name, add subject, delete subject

    # @strawberry.field(description="groups linked the program")
    # async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
    #     async with withInfo(info) as session:
    #         links = await resolveGroupIdsForProgram(session, self.id)
    #         result = list(map(lambda item: GroupGQLModel(id=item), links))
    #         return result


