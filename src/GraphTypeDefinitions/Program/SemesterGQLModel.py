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

SubjectGQLModel = typing.Annotated["SubjectGQLModel", strawberry.lazy(".SubjectGQLModel")]
TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy(".TopicGQLModel")]
TopicInputFilter = typing.Annotated["TopicInputFilter", strawberry.lazy(".TopicGQLModel")]

StudyPlanGQLModel = typing.Annotated["StudyPlanGQLModel", strawberry.lazy("..Plan.StudyPlanGQLModel")]
StudyPlanInputFilter = typing.Annotated["StudyPlanInputFilter", strawberry.lazy("..Plan.StudyPlanGQLModel")]


@createInputs  
@dataclasses.dataclass
class SemesterInputFilter:
    id: IDType
    name: str


@strawberry.federation.type(
    keys=["id"],
    description="""Semester entity, allows division of subject into smaller parts"""
    )
class SemesterGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).SemesterModel
    
    order: typing.Optional[int] = strawberry.field(
        description="order in same subject", 
        permission_classes=[OnlyForAuthentized]
    )

    mandatory: typing.Optional[bool] = strawberry.field(
        description="True if every student must pass this subject", 
        permission_classes=[OnlyForAuthentized]
    )

    credits: typing.Optional[int] = strawberry.field(
        description="credits", 
        permission_classes=[OnlyForAuthentized]
    )
    
    subject_id: typing.Optional[IDType] = strawberry.field(
        description="subject id", 
        permission_classes=[OnlyForAuthentized]
    )
    
    subject: typing.Optional["SubjectGQLModel"] = strawberry.field(
        description="subject", 
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["SubjectGQLModel"](fkey_field_name="subject_id")
    )

    prerequisites: typing.List["SubjectGQLModel"] = strawberry.field(
        description="subjects vhcin must be studied at first", 
        permission_classes=[OnlyForAuthentized]
    )

    topics: typing.List["TopicGQLModel"] = strawberry.field(
        description="""Semester topics""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["TopicGQLModel"](fkey_field_name="semester_id", whereType=TopicInputFilter)
    )

    plans: typing.List["StudyPlanGQLModel"] = strawberry.field(
        description="plans of study execution",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudyPlanGQLModel"](fkey_field_name="semester_id", whereType=StudyPlanInputFilter)
    )