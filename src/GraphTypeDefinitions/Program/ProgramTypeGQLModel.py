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


@createInputs
@dataclasses.dataclass
class ProgramTypeInputFilter:
    id: IDType
    name: str
    name_en: str
    level_id: IDType
    title_id: IDType
    language_id: IDType
    form_id: IDType


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

    level_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    level_type: typing.Optional["ProgramLevelTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramLevelTypeGQLModel](fkey_field_name="level_id")
    )

    title_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    title_type: typing.Optional["ProgramTitleTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramTitleTypeGQLModel](fkey_field_name="title_id")
    )    

    language_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    language_type: typing.Optional["ProgramLanguageTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramLanguageTypeGQLModel](fkey_field_name="language_id")
    )        

    form_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_type: typing.Optional["ProgramFormTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramFormTypeGQLModel](fkey_field_name="form_id")
    )        


@strawberry.interface(
    description=""
)
class ProgramTypeQuery:
    program_type_by_id: typing.Optional["ProgramTypeGQLModel"] = strawberry.field(
        description="returns programtype by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramTypeGQLModel.load_with_loader
    )

    program_type_page: typing.List["ProgramTypeGQLModel"] = strawberry.field(
        description="returns programtypes defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramTypeGQLModel"](whereType=ProgramTypeInputFilter)
    )


@strawberry.input(
    description="parameter for create operation"
)
class ProgramTypeInsertGQLModel:
    name: str = strawberry.field(
        description="name of the program_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class ProgramTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramTypeMutation:

    @strawberry.mutation(
        description="create a new program_type"
    )
    async def program_type_insert(self, info: strawberry.types.Info, program_type: ProgramTypeInsertGQLModel) -> typing.Union[ProgramTypeGQLModel, InsertError[ProgramTypeGQLModel]]:
        result = await Insert[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        return result
    
    @strawberry.mutation(
        description="updates existing program_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_type_update(self, info: strawberry.types.Info, program_type: ProgramTypeUpdateGQLModel) -> typing.Union[ProgramTypeGQLModel, UpdateError[ProgramTypeGQLModel]]:
        result = await Update[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        return result

    @strawberry.mutation(
        description="delete existing program_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_type_delete(self, info: strawberry.types.Info, program_type: ProgramTypeDeleteGQLModel) -> typing.Optional[DeleteError[ProgramTypeGQLModel]]:
        result = await Delete[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        return result

