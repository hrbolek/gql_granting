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


ProgramLevelTypeGQLModel = typing.Annotated["ProgramLevelTypeGQLModel", strawberry.lazy(".ProgramLevelTypeGQLModel")]
ProgramTitleTypeGQLModel = typing.Annotated["ProgramTitleTypeGQLModel", strawberry.lazy(".ProgramTitleTypeGQLModel")]
ProgramLanguageTypeGQLModel = typing.Annotated["ProgramLanguageTypeGQLModel", strawberry.lazy(".ProgramLanguageTypeGQLModel")]
ProgramFormTypeGQLModel = typing.Annotated["ProgramFormTypeGQLModel", strawberry.lazy(".ProgramFormTypeGQLModel")]

@strawberry.federation.type(
    description="Unites attributes into single type",
    keys=["id"]
)
class ProgramTypeGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramTypeModel

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
    
    level_type_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    level_type: typing.Optional["ProgramLevelTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    title_type_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    title_type: typing.Optional["ProgramTitleTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    

    language_type_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    language_type: typing.Optional["ProgramLanguageTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )        

    form_type_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_type: typing.Optional["ProgramFormTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )        