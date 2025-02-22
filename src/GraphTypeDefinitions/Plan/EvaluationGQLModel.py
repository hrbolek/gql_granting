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

StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy("..Student.StudentGQLModel")]
SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy("..Program.SemesterGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("..UserGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("..EventGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]


@createInputs
@dataclasses.dataclass
class EvaluationInputFilter:
    student_id: IDType
    examiner_id: IDType
    created: datetime.datetime
    semester_id: IDType
    attempt: int
    event_id: IDType


@strawberry.federation.type(
    description="Exam evaluation"
)
class EvaluationGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ClassificationModel
    
    points: typing.Optional[int] = strawberry.field(
        default=None,
        description="given points for this exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    grade: typing.Optional[str] = strawberry.field(
        default=None,
        description="given grade / mark",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="description given to student and exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    order: typing.Optional[int] = strawberry.field(
        default=None,
        description="index of attempt",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    passed: typing.Optional[bool] = strawberry.field(
        default=None,
        description="True if student passed this exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    student_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="id of the student",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    student: typing.Optional["StudentGQLModel"] = strawberry.field(
        description="student who is examined",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StudentGQLModel"](fkey_field_name="student_id")
    )

    examiner_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="who examined",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    examiner: typing.Optional["UserGQLModel"] = strawberry.field(
        description="Who examined",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["UserGQLModel"](fkey_field_name="examiner_id")
    )

    semester_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="to which semester / subject this examination belongs",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    semester: typing.Optional["SemesterGQLModel"] = strawberry.field(
        description="semester to which this examination belongs to",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["SemesterGQLModel"](fkey_field_name="semester_id")
    )

    exam_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="related exam conditions",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    exam: typing.Optional["ExamGQLModel"] = strawberry.field(
        description="related exam conditions",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ExamGQLModel"](fkey_field_name="exam_id")
    )

    event_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="the event when exam happened and evaluation has been stored",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event: typing.Optional["EventGQLModel"] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EventGQLModel"](fkey_field_name="event_id")
    )

    parent_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="id of exam which this is part",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    parent: typing.Optional["EvaluationGQLModel"] = strawberry.field(
        description="exam of which is this part",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["EvaluationGQLModel"](fkey_field_name="parent_id")
    )

    children: typing.List["EvaluationGQLModel"] = strawberry.field(
        description="sub parts of this evaluation",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EvaluationGQLModel"](fkey_field_name="parent_id", whereType=EvaluationInputFilter)
    )

    classificationlevel_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="Formal given grade",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    classificationplan_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="Exam plan",
        permission_classes=[
            OnlyForAuthentized
        ]
    )



@strawberry.interface(
    description=""
)
class EvaluationQuery:

    evaluation_by_id: typing.Optional[EvaluationGQLModel] = strawberry.field(
        description="find an evaluation by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=EvaluationGQLModel.load_with_loader
    )

    evaluation_page: typing.List[EvaluationGQLModel] = strawberry.field(
        description="list of evaluations",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[EvaluationGQLModel](whereType=EvaluationInputFilter)
    )


@strawberry.input(
    description="parameter for create"
)
class EvaluationInsertGQLModel:
    semester_id: IDType = strawberry.field(
        description="Which semester / subject is examined"
    )

    user_id: IDType = strawberry.field(description="Who is examined")
    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value")

@strawberry.input(
    description="parameter for update"
)
class EvaluationUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the evaluation to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    grade: typing.Optional[str] = strawberry.field(description="", default=None)

@strawberry.input(
    description="parameter for delete"
)
class EvaluationDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the evaluation to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class EvaluationMutation:

    @strawberry.mutation(
        description="inserts a new evaluation",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def evaluation_insert(self, info: strawberry.types.Info, evaluation: EvaluationInsertGQLModel) -> typing.Union[EvaluationGQLModel, InsertError[EvaluationGQLModel]]:
        result = await Insert[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result
    
    @strawberry.mutation(
        description="updates an existing evaluatio",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def evaluation_update(self, info: strawberry.types.Info, evaluation: EvaluationUpdateGQLModel) -> typing.Union[EvaluationGQLModel, UpdateError[EvaluationGQLModel]]:
        result = await Update[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result

    @strawberry.mutation(
        description="deletes an existing evaluation",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def evaluation_delete(self, info: strawberry.types.Info, evaluation: EvaluationUpdateGQLModel) -> typing.Optional[DeleteError[EvaluationGQLModel]]:
        result = await Delete[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result

