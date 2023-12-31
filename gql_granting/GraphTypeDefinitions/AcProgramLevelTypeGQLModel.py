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

@strawberry.federation.type(keys=["id"], description="bachelor, ...")
class AcProgramLevelTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programleveltypes
        return loader

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="Name of the program level")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="name in english")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="date of lastchange")
    def lastchange(self) -> str:
        return self.lastchange

#################################################
# Query
#################################################

@strawberry.field(description="""Finds a program level its id""")
async def program_level_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcProgramLevelTypeGQLModel", None]:
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, id)
        return result

