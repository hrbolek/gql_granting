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
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

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

from uoishelpers.resolvers import InputModelMixin

@strawberry.input(
    description="parameter for create operation"
)
class ProgramLevelTypeInsertGQLModel(InputModelMixin):
    getLoader = ProgramLevelTypeGQLModel.getLoader
    name: str = strawberry.field(
        description="name of the program_level_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class ProgramLevelTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_level_type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name of the program_level_type", default=None)
    length: typing.Optional[int] = strawberry.field(description="length of the program_level_type", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramLevelTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramLevelTypeMutation:

    @strawberry.mutation(
        description="create a new program_level_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ProgramLevelTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "studijní administrátor"
                ]
            ),
        ],
    )
    async def program_level_type_insert(
        self, 
        info: strawberry.types.Info, 
        program_level_type: ProgramLevelTypeInsertGQLModel
    ) -> typing.Union[ProgramLevelTypeGQLModel, InsertError[ProgramLevelTypeGQLModel]]:
        result = await Insert[ProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=program_level_type)
        return result
    
    @strawberry.mutation(
        description="updates existing program_level_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramLevelTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "studijní administrátor"
                ]
            ),
        ],
    )
    async def program_level_type_update(
        self, 
        info: strawberry.types.Info, 
        program_level_type: ProgramLevelTypeUpdateGQLModel
    ) -> typing.Union[ProgramLevelTypeGQLModel, UpdateError[ProgramLevelTypeGQLModel]]:
        result = await Update[ProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=program_level_type)
        return result

    @strawberry.mutation(
        description="delete existing program_level_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, ProgramLevelTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "studijní administrátor"
                ]
            ),
        ],
    )
    async def program_level_type_delete(
        self, 
        info: strawberry.types.Info, 
        program_level_type: ProgramLevelTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[ProgramLevelTypeGQLModel]]:
        result = await Delete[ProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=program_level_type)
        return result

