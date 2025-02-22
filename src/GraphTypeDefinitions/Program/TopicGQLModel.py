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

from ..BaseGQLModel import BaseGQLModel, IDType

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

@strawberry.input(
    description="parameter for create operation"
)
class TopicInsertGQLModel:
    name: str = strawberry.field(
        description="name of the topic"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class TopicUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

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

    @strawberry.mutation(
        description="create a new topic"
    )
    async def topic_insert(self, info: strawberry.types.Info, topic: TopicInsertGQLModel) -> typing.Union[TopicGQLModel, InsertError[TopicGQLModel]]:
        result = await Insert[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        return result
    
    @strawberry.mutation(
        description="updates existing topic",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def topic_update(self, info: strawberry.types.Info, topic: TopicUpdateGQLModel) -> typing.Union[TopicGQLModel, UpdateError[TopicGQLModel]]:
        result = await Update[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        return result

    @strawberry.mutation(
        description="delete existing topic",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def topic_delete(self, info: strawberry.types.Info, topic: TopicDeleteGQLModel) -> typing.Optional[DeleteError[TopicGQLModel]]:
        result = await Delete[TopicGQLModel].DoItSafeWay(info=info, entity=topic)
        return result

