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

from ..BaseGQLModel import BaseGQLModel, IDType


TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy(".TopicGQLModel")]

@createInputs
@dataclasses.dataclass
class LessonTypeInputFilter:
    id: IDType
    name: str
    name_en: str

@strawberry.federation.type(
    keys=["id"],
    description="""LessonType entity"""
    )
class LessonTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).LessonTypeModel

    name: typing.Optional[str] = strawberry.field(
        description="name",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="english name",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    abbr: typing.Optional[str] = strawberry.field(
        description="abbreviation",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )


@strawberry.interface(
    description=""
)
class LessonTypeQuery:
    lesson_type_by_id: typing.Optional["LessonTypeGQLModel"] = strawberry.field(
        description="returns lesson type by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=LessonTypeGQLModel.load_with_loader
    )

    lesson_type_page: typing.List["LessonTypeGQLModel"] = strawberry.field(
        description="returns lesson types defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["LessonTypeGQLModel"](whereType=LessonTypeInputFilter)
    )


@strawberry.input(
    description="parameter for create"
)
class LessonTypeInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the lesson_type.", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the lesson_type.", default=None
    )
    abbr: typing.Optional[str] = strawberry.field(
        description="Abbreviation of the lesson_type.", default=None
    )
    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value", default=None)

    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="parameter for update"
)
class LessonTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the lesson_type to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the lesson_type.", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the lesson_type.", default=None
    )
    abbr: typing.Optional[str] = strawberry.field(
        description="Abbreviation of the lesson_type.", default=None
    )

@strawberry.input(
    description="parameter for delete"
)
class LessonTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the lesson_type to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class LessonTypeMutation:

    @strawberry.mutation(
        description="inserts a new lesson_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, LessonTypeGQLModel](
                roles=["superadmin"]
            ),
            # UserAccessControlExtension[InsertError, LessonTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[InsertError, LessonTypeGQLModel](),
            # RbacProviderExtension[InsertError, LessonTypeGQLModel](),
            # LoadDataExtension[InsertError, LessonTypeGQLModel]()
        ]
    )
    async def lesson_type_insert(
        self, 
        info: strawberry.types.Info, 
        lesson_type: LessonTypeInsertGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[LessonTypeGQLModel, InsertError[LessonTypeGQLModel]]:
        return await Insert[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        
    
    @strawberry.mutation(
        description="updates an existing lesson_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, LessonTypeGQLModel](
                roles=["superadmin"]
            ),
            # UserAccessControlExtension[UpdateError, LessonTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[UpdateError, LessonTypeGQLModel](),
            # RbacProviderExtension[UpdateError, LessonTypeGQLModel](),
            # LoadDataExtension[UpdateError, LessonTypeGQLModel]()
        ]
    )
    async def lesson_type_update(
        self, 
        info: strawberry.types.Info, 
        lesson_type: LessonTypeUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Union[LessonTypeGQLModel, UpdateError[LessonTypeGQLModel]]:
        return await Update[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        

    @strawberry.mutation(
        description="deletes an existing lesson_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, LessonTypeGQLModel](
                roles=["superadmin"]
            ),
            # UserAccessControlExtension[DeleteError, LessonTypeGQLModel](roles=["administrátor", "personalista"]),
            # UserRoleProviderExtension[DeleteError, LessonTypeGQLModel](),
            # RbacProviderExtension[DeleteError, LessonTypeGQLModel](),
            # LoadDataExtension[DeleteError, LessonTypeGQLModel]()
        ]
    )
    async def lesson_type_delete(
        self, 
        info: strawberry.types.Info, 
        lesson_type: LessonTypeUpdateGQLModel,
        user_roles: typing.List[dict],
        # rbacobject_id: IDType,
        # db_row: typing.Any
    ) -> typing.Optional[DeleteError[LessonTypeGQLModel]]:
        return await Delete[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        

