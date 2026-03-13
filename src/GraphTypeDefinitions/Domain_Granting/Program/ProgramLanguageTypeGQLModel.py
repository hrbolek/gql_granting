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

from uoishelpers.resolvers import InputModelMixin

@strawberry.input(
    description="parameter for create operation"
)
class ProgramLanguageTypeInsertGQLModel(InputModelMixin):
    getLoader = ProgramLanguageTypeGQLModel.getLoader
    name: str = strawberry.field(
        description="name of the program_language_type"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the program_language_type",
        default=None
    )
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class ProgramLanguageTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_language_type", default=None)
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the program_language_type",
        default=None
    )

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
        description="create a new program_language_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramLanguageTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_language_type_insert(
        self, 
        info: strawberry.types.Info, 
        program_language_type: ProgramLanguageTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramLanguageTypeGQLModel, InsertError[ProgramLanguageTypeGQLModel]]:
        return await Insert[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        
    
    @strawberry.mutation(
        description="updates existing program_language_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramLanguageTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_language_type_update(
        self, 
        info: strawberry.types.Info, 
        program_language_type: ProgramLanguageTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramLanguageTypeGQLModel, UpdateError[ProgramLanguageTypeGQLModel]]:
        return await Update[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        

    @strawberry.mutation(
        description="delete existing program_language_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramLanguageTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_language_type_delete(
        self, 
        info: strawberry.types.Info, 
        program_language_type: ProgramLanguageTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProgramLanguageTypeGQLModel]]:
        return await Delete[ProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=program_language_type)
        

