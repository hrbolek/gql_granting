import uuid
import strawberry
import typing
import datetime
import logging
import asyncio
from uuid import UUID
from typing import Optional, List, Union, Annotated

from ..utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

#UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".granting")]

@strawberry.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).lessontype
        return loader

    @strawberry.field(description="primary key")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="name")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="english name")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="datetime lastchange")
    def lastchange(self) -> str:
        return self.lastchange
    
#################################################
#
# Special fields for query
#
#################################################

@strawberry.field(description="""Finds a lesson type by its id""")
async def aclesson_type_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union["AcLessonTypeGQLModel", None]:
        result = await AcLessonTypeGQLModel.resolve_reference(info, id)
        return result
@strawberry.field(description="""Gets all lesson types""")
async def aclesson_type_page(
        self, info: strawberry.types.Info
    ) -> List["AcLessonTypeGQLModel"]:
        loader = getLoaders(info).lessontypes
        rows = await loader.execute_select(loader.getSelectStatement())
        return rows

