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
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_: typing.Optional["LessonTypeGQLModel"] = strawberry.field(
        name="type",
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[LessonTypeGQLModel](fkey_field_name="topic_id")
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
