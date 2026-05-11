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


SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy(".SemesterGQLModel")]
LessonGQLModel = typing.Annotated["LessonGQLModel", strawberry.lazy(".LessonGQLModel")]
LessonInputFilter = typing.Annotated["LessonInputFilter", strawberry.lazy(".LessonGQLModel")]

@createInputs
@dataclasses.dataclass
class TopicInputFilter:
    id: IDType
    name: str

@strawberry.federation.type(
    keys=["id"],
    description="""Topic entity"""
    )
class TopicGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).TopicModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="topic name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="topic name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    order: typing.Optional[int] = strawberry.field(
        default=None,
        description="topic name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="topic description", 
        permission_classes=[OnlyForAuthentized]
        )
    
    semester_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="semester id", 
        permission_classes=[OnlyForAuthentized]
        )
    
    semester: typing.Optional["SemesterGQLModel"] = strawberry.field(
        description="semester", 
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["SemesterGQLModel"](fkey_field_name="semester_id")
        )
    
    lessons: typing.List["LessonGQLModel"] = strawberry.field(
        description="lessons", 
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["LessonGQLModel"](fkey_field_name="topic_id", whereType=LessonInputFilter)
        )
    

@strawberry.interface(
    description=""
)
class TopicQuery:
    topic_by_id: typing.Optional["TopicGQLModel"] = strawberry.field(
        description="returns topic by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=TopicGQLModel.load_with_loader
    )

    topic_page: typing.List["TopicGQLModel"] = strawberry.field(
        description="returns topics defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["TopicGQLModel"](whereType=TopicInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class TopicInsertGQLModel(InputModelMixin):
    getLoader = TopicGQLModel.getLoader
    semester_id: typing.Optional[IDType] = strawberry.field(
        description="semester id",
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="primary key client generated", default=None)
    name: typing.Optional[str] = strawberry.field(
        description="topic name", default=None)
    name_en: typing.Optional[str] = strawberry.field(
        description="topic name", default=None)
    order: typing.Optional[int] = strawberry.field(
        description="topic name", default=None)
    description: typing.Optional[str] = strawberry.field(
        description="topic description", default=None)

    from .LessonGQLModel import LessonInsertGQLModel
    lessons: typing.Optional[typing.List[LessonInsertGQLModel]] = strawberry.field(
        description="lessons",
        default_factory=list,
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None
    


@strawberry.input(
    description="parameter for update operation"
)
class TopicUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="topic name", default=strawberry.UNSET)
    name_en: typing.Optional[str] = strawberry.field(description="topic name", default=strawberry.UNSET)
    order: typing.Optional[int] = strawberry.field(description="topic name", default=strawberry.UNSET)
    description: typing.Optional[str] = strawberry.field(description="topic description", default=strawberry.UNSET)
    semester_id: typing.Optional[IDType] = strawberry.field(description="semester id", default=strawberry.UNSET)
    
@strawberry.input(
    description="parameter for delete operation"
)
class TopicDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class TopicMutation:
    from .SemesterGQLModel import SemesterGQLModel
    @strawberry.mutation(
        description="create a new topic",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, TopicGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[InsertError, TopicGQLModel](),
            RbacProviderExtension[InsertError, TopicGQLModel](),
            LoadDataExtension[InsertError, TopicGQLModel](
                primary_key_name="semester_id",
                getLoader=SemesterGQLModel.getLoader
            )
        ]
    )
    async def topic_insert(
        self, 
        info: strawberry.types.Info, 
        topic: TopicInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[TopicGQLModel, InsertError[TopicGQLModel]]:
        topic.rbacobject_id = rbacobject_id
        return await Insert[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        
    
    @strawberry.mutation(
        description="updates existing topic",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, TopicGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, TopicGQLModel](),
            RbacProviderExtension[UpdateError, TopicGQLModel](),
            LoadDataExtension[UpdateError, TopicGQLModel]()
        ]
    )
    async def topic_update(
        self, 
        info: strawberry.types.Info, 
        topic: TopicUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[TopicGQLModel, UpdateError[TopicGQLModel]]:
        return await Update[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        

    @strawberry.mutation(
        description="delete existing topic",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, TopicGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[DeleteError, TopicGQLModel](),
            RbacProviderExtension[DeleteError, TopicGQLModel](),
            LoadDataExtension[DeleteError, TopicGQLModel]()
        ]
    )
    async def topic_delete(
        self, 
        info: strawberry.types.Info, 
        topic: TopicDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[TopicGQLModel]]:
        return await Delete[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        

