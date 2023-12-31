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

@strawberry.federation.type(
    keys=["id"], description="Program form type (Present, distant, ...)"
)
class AcProgramFormTypeGQLModel:
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).programforms
        return loader

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="name")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="name")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="")
    def lastchange(self) -> str:
        return self.lastchange


#################################################
#
# Special fields for query
#
#################################################

@strawberry.field(description="""Finds a program from its id""")
async def program_form_by_id(
        self, info: strawberry.types.Info, id: UUID
    ) -> Union["AcProgramFormTypeGQLModel", None]:
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, id)
        return result


