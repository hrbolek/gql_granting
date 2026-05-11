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

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType


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

from uoishelpers.resolvers import InputModelMixin

@strawberry.input(
    description="parameter for create operation"
)
class ProgramTitleTypeInsertGQLModel(InputModelMixin):
    getLoader = ProgramTitleTypeGQLModel.getLoader
    name: str = strawberry.field(
        description="name of the program_title_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)

    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class ProgramTitleTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_title_type", default=strawberry.UNSET)
    name_en: typing.Optional[str] = strawberry.field(description="name of the program_title_type", default=strawberry.UNSET)

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
        description="create a new program_title_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ProgramTitleTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_title_type_insert(
        self, 
        info: strawberry.types.Info, 
        program_title_type: ProgramTitleTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramTitleTypeGQLModel, InsertError[ProgramTitleTypeGQLModel]]:
        return await Insert[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        
    
    @strawberry.mutation(
        description="updates existing program_title_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramTitleTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_title_type_update(
        self, 
        info: strawberry.types.Info, 
        program_title_type: ProgramTitleTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramTitleTypeGQLModel, UpdateError[ProgramTitleTypeGQLModel]]:
        return await Update[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        

    @strawberry.mutation(
        description="delete existing program_title_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, ProgramTitleTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_title_type_delete(
        self, 
        info: strawberry.types.Info, 
        program_title_type: ProgramTitleTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProgramTitleTypeGQLModel]]:
        return await Delete[ProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=program_title_type)
        

