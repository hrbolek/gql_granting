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
        loader = getLoadersFromInfo(info).programlanguages
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


from gql_granting.GraphResolvers import resolveLanguageTypeById


@strawberry.federation.type(keys=["id"], description="Study program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).programlanguages
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="name (like čeština)")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="name (like Czech)")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
#################################################
#
# Special fields for query
#
#################################################
@strawberry.field(description="""Finds a program language its id""")
async def program_language_by_id(
        self, info: strawberry.types.Info, id:UUID
    ) -> Union["AcProgramLanguageTypeGQLModel", None]:
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, id)
        return result

