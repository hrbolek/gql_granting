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
    description="Classification level aka 'A', 'B', ..."
)
class ClassificationLevelGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ClassificationLevelModel
    
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
    
    ordervalue: typing.Optional[int] = strawberry.field(
        default=None,
        description="to make the name convertible to number",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    

@strawberry.interface(description="base queries")
class ClassificationLevelQueries:
    @strawberry.field(
        description="get classification level by id",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def classification_level_by_id(self, info: strawberry.types.Info, id: IDType) -> ClassificationLevelGQLModel:
        return await ClassificationLevelGQLModel.resolve_reference(info=info, id=id)

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(description="")
class ClassificationLevelInsertGQLModel(InputModelMixin):
    getLoader = ClassificationLevelGQLModel.getLoader
    name: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the classification",
        default=None
    )    
    ordervalue: typing.Optional[int] = strawberry.field(
        description="to make the name convertible to number",
        default=None
    )    
    id: typing.Optional[IDType] = strawberry.field(
        description="optional client generated primary key",
        default=None
    )

@strawberry.input(description="")
class ClassificationLevelUpdateGQLModel:
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
    ordervalue: typing.Optional[int] = strawberry.field(
        description="to make the name convertible to number",
        default=None
    )    

@strawberry.input(description="")
class ClassificationLevelDeleteGQLModel:
    id: IDType = strawberry.field(
        description="primary key"
    )
    lastchange: datetime.datetime = strawberry.field(
        description="time stamp for concurent updates"
    )

@strawberry.interface(
    description="base ClassificationLevel mutations"
)
class ClassificationLevelMutations:
    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ClassificationLevelGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[InsertError, ClassificationLevelGQLModel](
            #     roles=[
            #         # "administrátor", 
            #         "studijní administrátor"
            #     ]
            # ),
            # UserRoleProviderExtension[InsertError, ClassificationLevelGQLModel](),
            # RbacProviderExtension[InsertError, ClassificationLevelGQLModel](),
            # LoadDataExtension[InsertError, ClassificationLevelGQLModel]()
        ]
    )
    async def classification_level_insert(
        self,
        info: strawberry.types.Info,
        classification_level: ClassificationLevelInsertGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[InsertError[ClassificationLevelGQLModel], ClassificationLevelGQLModel]:
        result = await Insert[ClassificationLevelGQLModel].DoItSafeWay(
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
            UserAbsoluteAccessControlExtension[InsertError, ClassificationLevelGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[UpdateError, ClassificationLevelGQLModel](
            #     roles=[
            #         # "administrátor", 
            #         "studijní administrátor"
            #     ]
            # ),
            # UserRoleProviderExtension[UpdateError, ClassificationLevelGQLModel](),
            # RbacProviderExtension[UpdateError, ClassificationLevelGQLModel](),
            # LoadDataExtension[UpdateError, ClassificationLevelGQLModel]()
        ]
    )
    async def classification_level_update(
        self,
        info: strawberry.types.Info,
        classification_level: ClassificationLevelUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[UpdateError[ClassificationLevelGQLModel], ClassificationLevelGQLModel]:
        result = await Update[ClassificationLevelGQLModel].DoItSafeWay(
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
            UserAbsoluteAccessControlExtension[InsertError, ClassificationLevelGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
            # UserAccessControlExtension[DeleteError, ClassificationLevelGQLModel](
            #     roles=[
            #         "studijní administrátor", 
            #         # "personalista"
            #     ]
            # ),
            # UserRoleProviderExtension[DeleteError, ClassificationLevelGQLModel](),
            # RbacProviderExtension[DeleteError, ClassificationLevelGQLModel](),
            # LoadDataExtension[DeleteError, ClassificationLevelGQLModel]()
        ]
    )
    async def classification_level_delete(
        self,
        info: strawberry.types.Info,
        classification_level: ClassificationLevelUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Optional[DeleteError[ClassificationLevelGQLModel]]:
        result = await Delete[ClassificationLevelGQLModel].DoItSafeWay(
            info=info,
            entity=classification_level
        )
        return result