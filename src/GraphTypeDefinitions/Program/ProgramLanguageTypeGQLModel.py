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


@strawberry.input(
    description="parameter for create operation"
)
class ProgramLanguageTypeInsertGQLModel:
    name: str = strawberry.field(
        description="name of the program_language_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class ProgramLanguageTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_language_type", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramLanguageTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramLanguageTypeMutation:

    @strawberry.mutation(
        description="create a new program_language_type"
    )
    async def program_language_type_insert(self, info: strawberry.types.Info, program_language_type: ProgramLanguageTypeInsertGQLModel) -> typing.Union[ProgramLanguageTypeGQLModel, InsertError[ProgramLanguageTypeGQLModel]]:
        result = await Insert[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        return result
    
    @strawberry.mutation(
        description="updates existing program_language_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_language_type_update(self, info: strawberry.types.Info, program_language_type: ProgramLanguageTypeUpdateGQLModel) -> typing.Union[ProgramLanguageTypeGQLModel, UpdateError[ProgramLanguageTypeGQLModel]]:
        result = await Update[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        return result

    @strawberry.mutation(
        description="delete existing program_language_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_language_type_delete(self, info: strawberry.types.Info, program_language_type: ProgramLanguageTypeDeleteGQLModel) -> typing.Optional[DeleteError[ProgramLanguageTypeGQLModel]]:
        result = await Delete[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        return result

