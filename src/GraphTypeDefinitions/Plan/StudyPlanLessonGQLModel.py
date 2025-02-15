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

from ..BaseGQLModel import BaseGQLModel, IDType

TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy("..Program.TopicGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("..UserGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("..GroupGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy("..FacilityGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("..EventGQLModel")]

@createInputs
@dataclasses.dataclass
class StudyPlanLessonInputFilter:
    id: IDType
    name: str

@strawberry.federation.type(
    description="On row in studyplan"
)
class StudyPlanLessonGQLModel(BaseGQLModel):

    order: typing.Optional[int] = strawberry.field(
        description="order in plan",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    length: typing.Optional[int] = strawberry.field(
        description="length in fictive units",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event_id: typing.Optional[IDType] = strawberry.field(
        description="id of event which has been planed for this lesson",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event: typing.Optional["EventGQLModel"] = strawberry.field(
        description="event which has been planed for this lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EventGQLModel"](fkey_field_name="event_id")
    )

    topic_id: typing.Optional[IDType] = strawberry.field(
        description="Topic to which the Lesson is related",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    topic: typing.Optional["TopicGQLModel"] =strawberry.field(
        description="Topic to which the Lesson is related",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["TopicGQLModel"](fkey_field_name="topic_id")
    )

    linked_with_id: typing.Optional[IDType] = strawberry.type(
        description="key to describe integration with other planned lessons"
    )

    @strawberry.field(
        description="list of linked othe planned lessons",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def linked_with(self, info: strawberry.types.Info) -> typing.List["StudyPlanLessonGQLModel"]:
        return []
    
    @strawberry.field(
        description="whos teach the lesson",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def instructors(self, info: strawberry.types.Info) -> typing.List["UserGQLModel"]:
        return []

    @strawberry.field(
        description="study groups",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def study_groups(self, info: strawberry.types.Info) -> typing.List["GroupGQLModel"]:
        return []
    
    @strawberry.field(
        description="places for this lesson",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def facilities(self, info: strawberry.types.Info) -> typing.List["FacilityGQLModel"]:
        return []