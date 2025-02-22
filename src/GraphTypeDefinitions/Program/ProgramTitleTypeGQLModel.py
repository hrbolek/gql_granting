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

@createInputs
@dataclasses.dataclass
class ProgramTitleTypeInputFilter:
    id: IDType
    name: str
    name_en: str


@strawberry.federation.type(
    description="Specifies title if ended successfully",
    keys=["id"]
)
class ProgramTitleTypeGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramTitleTypeModel

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

@strawberry.interface(
    description=""
)
class ProgramTitleQuery:
    program_title_by_id: typing.Optional["ProgramTitleTypeGQLModel"] = strawberry.field(
        description="returns programtitle by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramTitleTypeGQLModel.load_with_loader
    )

    program_title_page: typing.List["ProgramTitleTypeGQLModel"] = strawberry.field(
        description="returns programtitles defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramTitleTypeGQLModel"](whereType=ProgramTitleTypeInputFilter)
    )