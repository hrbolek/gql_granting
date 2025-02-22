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
class ProgramLanguageTypeInputFilter:
    id: IDType
    name: str
    name_en: str



@strawberry.federation.type(
    description="language definition, often CZ or EN",
    keys=["id"]
)
class ProgramLanguageTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramLanguageTypeModel

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
class ProgramLanguageQuery:
    program_language_by_id: typing.Optional["ProgramLanguageTypeGQLModel"] = strawberry.field(
        description="returns programlanguage by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramLanguageTypeGQLModel.load_with_loader
    )

    program_language_page: typing.List["ProgramLanguageTypeGQLModel"] = strawberry.field(
        description="returns programlanguages defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramLanguageTypeGQLModel"](whereType=ProgramLanguageTypeInputFilter)
    )    