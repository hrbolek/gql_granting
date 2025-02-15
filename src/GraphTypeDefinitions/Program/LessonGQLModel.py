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
    
    topic_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    topic: typing.Optional["TopicGQLModel"] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["TopicGQLModel"](fkey_field_name="topic_id")
    )