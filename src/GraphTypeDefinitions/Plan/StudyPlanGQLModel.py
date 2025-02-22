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

SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy("..Program.SemesterGQLModel")]
StudyPlanLessonGQLModel = typing.Annotated["StudyPlanLessonGQLModel", strawberry.lazy(".StudyPlanLessonGQLModel")]
StudyPlanLessonInputFilter = typing.Annotated["StudyPlanLessonInputFilter", strawberry.lazy(".StudyPlanLessonGQLModel")]

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
# ExamInputFilter = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("..EventGQLModel")]

@createInputs
@dataclasses.dataclass
class StudyPlanInputFilter:
    id: IDType
    semester_id: IDType
    exam_id: IDType
    event_id: IDType


@strawberry.federation.type()
class StudyPlanGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).PlanModel
    
    semester_id: typing.Optional[IDType] = strawberry.field(
        description="ID of Semester to which the plan is related",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    semester: typing.Optional["SemesterGQLModel"] = strawberry.field(
        description="Semester to which the plan is related",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["SemesterGQLModel"](fkey_field_name="semester_id")
    )

    lessons: typing.List["StudyPlanLessonGQLModel"] = strawberry.field(
        description="part of study plan",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudyPlanLessonGQLModel"](fkey_field_name="semester_id", whereType=StudyPlanLessonInputFilter)
    )

    exam_id: typing.Optional[IDType] = strawberry.field(
        description="Exam Rules",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    exam: typing.Optional["ExamGQLModel"] = strawberry.field(
        description="Exam Rules",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ExamGQLModel"](fkey_field_name="plan_id")
    )

    event_id: typing.Optional[IDType] = strawberry.field(
        description="Time period when the plan will live",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event: typing.Optional["EventGQLModel"] = strawberry.field(
        description="Time period when the plan will live",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EventGQLModel"](fkey_field_name="event_id")
    )

@strawberry.interface()
class StudyPlanQuery:
    studyplan_page: typing.List[StudyPlanGQLModel] = strawberry.field(
        description="filtered list of study plan",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[StudyPlanGQLModel](whereType=StudyPlanInputFilter)
    )
