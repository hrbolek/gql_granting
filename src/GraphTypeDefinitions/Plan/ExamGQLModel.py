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

EvaluationGQLModel = typing.Annotated["EvaluationGQLModel", strawberry.lazy(".EvaluationGQLModel")]
EvaluationInputFilter = typing.Annotated["EvaluationInputFilter", strawberry.lazy(".EvaluationGQLModel")]

@createInputs
@dataclasses.dataclass
class ExamInputFilter:
    id: IDType



@strawberry.federation.type(
    keys=["id"],
    description="Exam definition"
)
class ExamGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ExamModel
    
    name: typing.Optional[str] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        description="extended description of exam conditions",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    min_score: typing.Optional[int] = strawberry.field(
        description="defined minimum points to pass the exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    max_score: typing.Optional[int] = strawberry.field(
        description="defined maximum achievable points"
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        description="id of exam which is part"
    )

    parent: typing.Optional[IDType] = strawberry.field(
        description="exam is part of exam",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ExamGQLModel"](fkey_field_name="parent_id")
    )

    parts: typing.List["ExamGQLModel"] = strawberry.field(
        description="exam parts",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["ExamGQLModel"](fkey_field_name="parent_id", whereType=ExamInputFilter)
    )

    evaluations: typing.List["EvaluationGQLModel"] = strawberry.field(
        description="evaluations of users during exams",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EvaluationGQLModel"](fkey_field_name="exam_id", whereType=EvaluationInputFilter)
    )