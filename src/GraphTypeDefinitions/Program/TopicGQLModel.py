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
        description="topic name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description: typing.Optional[str] = strawberry.field(
        description="topic description", 
        permission_classes=[OnlyForAuthentized]
        )
    
    semester_id: typing.Optional[IDType] = strawberry.field(
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