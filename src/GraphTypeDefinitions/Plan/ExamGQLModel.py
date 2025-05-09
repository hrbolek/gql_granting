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
StudyPlanGQLModel = typing.Annotated["StudyPlanGQLModel", strawberry.lazy(".StudyPlanGQLModel")]

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
    
    # plan_id: typing.Optional[IDType] = strawberry.field(
    #     default=None,
    #     description="study plan which the exam belongs to",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ]
    # )

    @strawberry.field(
        description="study plan which the exam belongs to",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def plan_id(self, info: strawberry.types.Info) -> typing.Optional[IDType]:
        from .StudyPlanGQLModel import StudyPlanGQLModel
        planLoader = StudyPlanGQLModel.getLoader(info)
        planRows = await planLoader.filter_by(classificationplan_id=self.id)
        planRow = next(planRows, None)
        return planRow.id if planRow else None

    @strawberry.field(
        description="study plan which the exam belongs to",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def plan(self, info: strawberry.types.Info) -> typing.Optional["StudyPlanGQLModel"]:
        from .StudyPlanGQLModel import StudyPlanGQLModel
        planLoader = StudyPlanGQLModel.getLoader(info)
        planRows = await planLoader.filter_by(classificationplan_id=self.id)
        planRow = next(planRows, None)
        return StudyPlanGQLModel.from_dataclass(planRow) if planRow else None

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

    parent: typing.Optional["ExamGQLModel"] = strawberry.field(
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

    exam_by_id: typing.Optional[ExamGQLModel] = strawberry.field(
        description="Exam by it id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ExamGQLModel.load_with_loader
    )

    exam_page: typing.List[ExamGQLModel] = strawberry.field(
        description="filtered exams",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[ExamGQLModel](whereType=ExamInputFilter)
    )


@strawberry.input(
    description="parameter for create"
)
class ExamInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the exam.", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the exam.", default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="A detailed localized description of the exam.", default=None
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="A detailed description of the exam in English.", default=None
    )
    min_score: typing.Optional[int] = strawberry.field(
        description="The minimum score required, used for passing or grading.", default=None
    )
    max_score: typing.Optional[int] = strawberry.field(
        description="The maximum achievable score for the exam.", default=None
    )
    type_id: typing.Optional[IDType] = strawberry.field(
        description="Identifier for the exam type, which determines its category or format.", default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier for a parent exam, if applicable.", default=None
    )
    plan_id: typing.Optional[IDType] = strawberry.field(
        description="Identifier for the exam plan or schedule this exam belongs to.", default=None
    )   
    id: typing.Optional[IDType] = strawberry.field(
        description="optional client generated primary key value", default=None
    )

    semester_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="parameter for update"
)
class ExamUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the exam to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the exam.", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the exam.", default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="A detailed localized description of the exam.", default=None
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="A detailed description of the exam in English.", default=None
    )
    min_score: typing.Optional[int] = strawberry.field(
        description="The minimum score required, used for passing or grading.", default=None
    )
    max_score: typing.Optional[int] = strawberry.field(
        description="The maximum achievable score for the exam.", default=None
    )
    type_id: typing.Optional[IDType] = strawberry.field(
        description="Identifier for the exam type, which determines its category or format.", default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier for a parent exam, if applicable.", default=None
    )
    plan_id: typing.Optional[IDType] = strawberry.field(
        description="Identifier for the exam plan or schedule this exam belongs to.", default=None
    )

@strawberry.input(
    description="parameter for delete"
)
class ExamDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the exam to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class ExamMutation:

    @strawberry.mutation(
        description="inserts a new exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def exam_insert(self, info: strawberry.types.Info, exam: ExamInsertGQLModel) -> typing.Union[ExamGQLModel, InsertError[ExamGQLModel]]:
        #TODO implement plan update to accept examid
        result = await Insert[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
        if getattr(result, "failed", False):
            return result
        
        from .StudyPlanGQLModel import StudyPlanGQLModel, StudyPlanUpdateGQLModel
        if exam.plan_id is None:
            return result
        planEntity = StudyPlanUpdateGQLModel(id=exam.plan_id, exam_id=result.id)
        planResult = await Update[StudyPlanGQLModel].DoItSafeWay(info=info, entity=planEntity)
        if getattr(planResult, "failed", False):
            return InsertError[ExamGQLModel](
                msg=planResult.msg,
                _input=exam
            )
        return result
    
    @strawberry.mutation(
        description="updates an existing evaluatio",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def exam_update(self, info: strawberry.types.Info, exam: ExamUpdateGQLModel) -> typing.Union[ExamGQLModel, UpdateError[ExamGQLModel]]:
        result = await Update[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
        return result

    @strawberry.mutation(
        description="deletes an existing exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def exam_delete(self, info: strawberry.types.Info, exam: ExamUpdateGQLModel) -> typing.Optional[DeleteError[ExamGQLModel]]:
        result = await Delete[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
        return result

