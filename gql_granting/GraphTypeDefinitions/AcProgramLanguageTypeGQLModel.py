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

@strawberry.federation.type(keys=["id"], description="Study program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programlanguages
        return loader

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="name (like čeština)")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="name (like Czech)")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="date of lastchange")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
#################################################
# Query
#################################################

@strawberry.field(description="""Finds a program language its id""")
async def program_language_by_id(
        self, info: strawberry.types.Info, id:UUID
    ) -> Union["AcProgramLanguageTypeGQLModel", None]:
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, id)
        return result

