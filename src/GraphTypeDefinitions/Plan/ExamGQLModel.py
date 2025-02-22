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
    parent_id: IDType
    name: str
    description: str
    min_score: int
    max_score: int



@strawberry.federation.type(
    keys=["id"],
    description="Exam definition"
)
class ExamGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ClassificationPlanModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="extended description of exam conditions",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="extended description of exam conditions",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    min_score: typing.Optional[int] = strawberry.field(
        default=None,
        description="defined minimum points to pass the exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    max_score: typing.Optional[int] = strawberry.field(
        default=None,
        description="defined maximum achievable points",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="id of exam type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="id of exam which is part",
        permission_classes=[
            OnlyForAuthentized
        ]
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

@strawberry.interface(
    description=""
)
class ExamQuery:

    exam_page: typing.List[ExamGQLModel] = strawberry.field(
        description="filtered evaluations",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[ExamGQLModel](whereType=ExamInputFilter)
    )