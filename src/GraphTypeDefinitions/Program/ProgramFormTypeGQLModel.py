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

ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy(".ProgramGQLModel")]
ProgramInputFilter = typing.Annotated["ProgramInputFilter", strawberry.lazy(".ProgramGQLModel")]

@createInputs
@dataclasses.dataclass
class ProgramFormTypeInputFilter:
    id: IDType
    name: str
    name_en: str

@strawberry.federation.type(
    description="Describes the form of Program, something like Distant",
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


@strawberry.interface(
    description=""
)
class ProgramFormTypeQuery:
    program_form_by_id: typing.Optional["ProgramFormTypeGQLModel"] = strawberry.field(
        description="returns programform by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramFormTypeGQLModel.load_with_loader
    )

    program_form_page: typing.List["ProgramFormTypeGQLModel"] = strawberry.field(
        description="returns programforms defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramFormTypeGQLModel"](whereType=ProgramFormTypeInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin

@strawberry.input(
    description="parameter for create operation"
)
class ProgramFormTypeInsertGQLModel(InputModelMixin):
    getLoader = ProgramFormTypeGQLModel.getLoader
    name: str = strawberry.field(
        description="name of the program_form_type"
    )
    name_en: str = strawberry.field(
        description="name of the program_form_type",
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)

    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class ProgramFormTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_form_type", default=None)
    name_en: str = strawberry.field(
        description="name of the program_form_type",
        default=None
    )

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramFormTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramFormTypeMutation:

    @strawberry.mutation(
        description="create a new program_form_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramFormTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_form_type_insert(
        self, 
        info: strawberry.types.Info, 
        program_form_type: ProgramFormTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramFormTypeGQLModel, InsertError[ProgramFormTypeGQLModel]]:
        return await Insert[ProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=program_form_type)
        
    
    @strawberry.mutation(
        description="updates existing program_form_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramFormTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_form_type_update(
        self, 
        info: strawberry.types.Info, 
        program_form_type: ProgramFormTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramFormTypeGQLModel, UpdateError[ProgramFormTypeGQLModel]]:
        return await Update[ProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=program_form_type)
        

    @strawberry.mutation(
        description="delete existing program_form_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, ProgramFormTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_form_type_delete(
        self, 
        info: strawberry.types.Info, 
        program_form_type: ProgramFormTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProgramFormTypeGQLModel]]:
        return await Delete[ProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=program_form_type)
        

