import asyncio
import dataclasses
import datetime
import typing
import strawberry

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



@strawberry.federation.type(
    keys=["id"],
    description="Classification type"
)
class ClassificationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ClassificationTypeModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="the name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="the name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    
    

@strawberry.interface(description="base queries")
class ClassificationTypeQueries:
    @strawberry.field(
        description="get classification type by id",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def classificationType_by_id(self, info: strawberry.types.Info, id: IDType) -> ClassificationTypeGQLModel:
        return await ClassificationTypeGQLModel.resolve_reference(info=info, id=id)

@strawberry.input(description="")
class ClassificationTypeInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )    
    name: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )    
    id: typing.Optional[IDType] = strawberry.field(
        description="optional client generated primary key",
        default=None
    )

@strawberry.input(description="")
class ClassificationTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="primary key"
    )
    lastchange: datetime.datetime = strawberry.field(
        description="time stamp for concurent updates"
    )
    name: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )    
    name: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )    

@strawberry.input(description="")
class ClassificationTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="primary key"
    )
    lastchange: datetime.datetime = strawberry.field(
        description="time stamp for concurent updates"
    )

@strawberry.interface(
    description="base ClassificationType mutations"
)
class ClassificationTypeMutations:
    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ClassificationTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[InsertError, ClassificationTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[InsertError, ClassificationTypeGQLModel](),
            # RbacProviderExtension[InsertError, ClassificationTypeGQLModel](),
            # LoadDataExtension[InsertError, ClassificationTypeGQLModel]()
        ]
    )
    async def classification_type_insert(
        self,
        info: strawberry.types.Info,
        classification_level: ClassificationTypeInsertGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[InsertError[ClassificationTypeGQLModel], ClassificationTypeGQLModel]:
        result = await Insert[ClassificationTypeGQLModel].DoItSafeWay(
            info=info,
            entity=classification_level
        )
        return result
    
    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ClassificationTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[UpdateError, ClassificationTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[UpdateError, ClassificationTypeGQLModel](),
            # RbacProviderExtension[UpdateError, ClassificationTypeGQLModel](),
            # LoadDataExtension[UpdateError, ClassificationTypeGQLModel]()
        ]
    )
    async def classification_type_update(
        self,
        info: strawberry.types.Info,
        classification_type: ClassificationTypeUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[UpdateError[ClassificationTypeGQLModel], ClassificationTypeGQLModel]:
        result = await Update[ClassificationTypeGQLModel].DoItSafeWay(
            info=info,
            entity=classification_type
        )
        return result
    
    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, ClassificationTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[DeleteError, ClassificationTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[DeleteError, ClassificationTypeGQLModel](),
            # RbacProviderExtension[DeleteError, ClassificationTypeGQLModel](),
            # LoadDataExtension[DeleteError, ClassificationTypeGQLModel]()
        ]
    )
    async def classification_type_delete(
        self,
        info: strawberry.types.Info,
        classification_type: ClassificationTypeUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Optional[DeleteError[ClassificationTypeGQLModel]]:
        result = await Delete[ClassificationTypeGQLModel].DoItSafeWay(
            info=info,
            entity=classification_type
        )
        return result