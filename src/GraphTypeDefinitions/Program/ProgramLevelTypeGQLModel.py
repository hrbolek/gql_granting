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
class ProgramLevelTypeInputFilter:
    id: IDType
    name: str
    name_en: str


@strawberry.federation.type(
    description="determine Bc. / Mgr. / Ph.D.",
    keys=["id"]
)
class ProgramLevelTypeGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramLevelTypeModel

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

    length: typing.Optional[int] = strawberry.field(
        description="how many years for standard study",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    priority: typing.Optional[int] = strawberry.field(
        description="1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D., etc.",
        permission_classes=[
            OnlyForAuthentized
        ]
    )


@strawberry.interface(
    description=""
)
class ProgramLevelQuery:
    program_level_by_id: typing.Optional["ProgramLevelTypeGQLModel"] = strawberry.field(
        description="returns programlevel by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramLevelTypeGQLModel.load_with_loader
    )

    program_level_page: typing.List["ProgramLevelTypeGQLModel"] = strawberry.field(
        description="returns programlevels defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramLevelTypeGQLModel"](whereType=ProgramLevelTypeInputFilter)
    )    