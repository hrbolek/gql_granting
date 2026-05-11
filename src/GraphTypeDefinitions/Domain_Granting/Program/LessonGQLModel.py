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



TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy(".TopicGQLModel")]
LessonTypeGQLModel = typing.Annotated["LessonTypeGQLModel", strawberry.lazy(".LessonTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class LessonInputFilter:
    id: IDType
    name: str

@strawberry.federation.type(
    keys=["id"],
    description="""Lesson entity"""
    )
class LessonGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).LessonModel
    
    count: typing.Optional[int] = strawberry.field(
        default=None,
        description="how many virtual time units",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    topic_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="to which topic belongs",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    topic: typing.Optional["TopicGQLModel"] = strawberry.field(
        description="to which topic belongs",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[TopicGQLModel](fkey_field_name="topic_id")
    )

    type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="type of Lesson, like Laboratories",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_: typing.Optional["LessonTypeGQLModel"] = strawberry.field(
        name="type",
        description="type of Lesson, like Laboratories",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[LessonTypeGQLModel](fkey_field_name="type_id")
    )

@strawberry.interface(
    description=""
)
class LessonQuery:
    lesson_by_id: typing.Optional["LessonGQLModel"] = strawberry.field(
        description="returns lesson by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=LessonGQLModel.load_with_loader
    )

    lesson_page: typing.List["LessonGQLModel"] = strawberry.field(
        description="returns lessons defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["LessonGQLModel"](whereType=LessonInputFilter)
    )


@strawberry.input(
    description="parameter for create"
)
class LessonInsertGQLModel:
    topic_id: typing.Optional[IDType] = strawberry.field(
        description="to which topic belongs", 
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value", default=None)
    count: typing.Optional[int] = strawberry.field(description="how many virtual time units", default=None)
    type_id: typing.Optional[IDType] = strawberry.field(description="lesson typ", default=None)
    rbacobject_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="parameter for update"
)
class LessonUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the lesson to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    count: typing.Optional[int] = strawberry.field(description="how many virtual time units", default=strawberry.UNSET)
    topic_id: typing.Optional[IDType] = strawberry.field(description="to which topic belongs", default=strawberry.UNSET)
    type_id: typing.Optional[IDType] = strawberry.field(description="lesson typ", default=strawberry.UNSET)

@strawberry.input(
    description="parameter for delete"
)
class LessonDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the lesson to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class LessonMutation:
    from .TopicGQLModel import TopicGQLModel
    @strawberry.mutation(
        description="inserts a new lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, LessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[InsertError, LessonGQLModel](),
            RbacProviderExtension[InsertError, LessonGQLModel](),
            LoadDataExtension[InsertError, LessonGQLModel](
                primary_key_name="topic_id",
                getLoader=TopicGQLModel.getLoader
            )
        ]
    )
    async def lesson_insert(
        self, 
        info: strawberry.types.Info, 
        lesson: LessonInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[LessonGQLModel, InsertError[LessonGQLModel]]:
        # TODO: check permissions for topic
        # lesson.rba
        return await Insert[LessonGQLModel].DoItSafeWay(info=info, entity=lesson)
        
    
    @strawberry.mutation(
        description="updates an existing evaluatio",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, LessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, LessonGQLModel](),
            RbacProviderExtension[UpdateError, LessonGQLModel](),
            LoadDataExtension[UpdateError, LessonGQLModel]()
        ]
    )
    async def lesson_update(
        self, 
        info: strawberry.types.Info, 
        lesson: LessonUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[LessonGQLModel, UpdateError[LessonGQLModel]]:
        return await Update[LessonGQLModel].DoItSafeWay(info=info, entity=lesson)
        

    @strawberry.mutation(
        description="deletes an existing lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, LessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[DeleteError, LessonGQLModel](),
            RbacProviderExtension[DeleteError, LessonGQLModel](),
            LoadDataExtension[DeleteError, LessonGQLModel]()
        ]
    )
    async def lesson_delete(
        self, 
        info: strawberry.types.Info, 
        lesson: LessonUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[LessonGQLModel]]:
        return await Delete[LessonGQLModel].DoItSafeWay(info=info, entity=lesson)

