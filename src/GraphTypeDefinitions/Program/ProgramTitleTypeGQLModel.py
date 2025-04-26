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


@strawberry.input(
    description="parameter for create operation"
)
class ProgramTitleTypeInsertGQLModel:
    name: str = strawberry.field(
        description="name of the program_title_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class ProgramTitleTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_title_type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name of the program_title_type", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramTitleTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramTitleTypeMutation:

    @strawberry.mutation(
        description="create a new program_title_type"
    )
    async def program_title_type_insert(self, info: strawberry.types.Info, program_title_type: ProgramTitleTypeInsertGQLModel) -> typing.Union[ProgramTitleTypeGQLModel, InsertError[ProgramTitleTypeGQLModel]]:
        result = await Insert[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        return result
    
    @strawberry.mutation(
        description="updates existing program_title_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_title_type_update(self, info: strawberry.types.Info, program_title_type: ProgramTitleTypeUpdateGQLModel) -> typing.Union[ProgramTitleTypeGQLModel, UpdateError[ProgramTitleTypeGQLModel]]:
        result = await Update[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        return result

    @strawberry.mutation(
        description="delete existing program_title_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_title_type_delete(self, info: strawberry.types.Info, program_title_type: ProgramTitleTypeDeleteGQLModel) -> typing.Optional[DeleteError[ProgramTitleTypeGQLModel]]:
        result = await Delete[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        return result

