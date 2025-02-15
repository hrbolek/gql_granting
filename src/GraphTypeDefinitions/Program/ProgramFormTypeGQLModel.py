import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

from ..BaseGQLModel import BaseGQLModel, IDType

ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy(".ProgramGQLModel")]
ProgramInputFilter = typing.Annotated["ProgramInputFilter", strawberry.lazy(".ProgramGQLModel")]

@strawberry.federation.type(
    description="",
    keys=["id"]
)
class ProgramFormTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramFormTypeModel
    
    name: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="english name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )