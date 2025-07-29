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
    createInputs2,

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

from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from ..BaseGQLModel import BaseGQLModel, IDType

StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy("..Student.StudentGQLModel")]
SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy("..Program.SemesterGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("..UserGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("..EventGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
ClassificationLevelGQLModel = typing.Annotated["ClassificationLevelGQLModel", strawberry.lazy("..Program.ClassificationLevelGQLModel")]

SemesterInputFilter = typing.Annotated["SemesterInputFilter", strawberry.lazy("..Program.SemesterGQLModel")]
StudentInputFilter = typing.Annotated["StudentInputFilter", strawberry.lazy("..Student.StudentGQLModel")]
ExamInputFilter = typing.Annotated["ExamInputFilter", strawberry.lazy(".ExamGQLModel")]

@createInputs2
class EvaluationInputFilter:
    order: int
    points: int
    passed: bool
    description: str

    classificationlevel_id: IDType
    exam_id: IDType
    semester_id: IDType
    parent_id: IDType
    student_id: IDType
    # user_id: IDType
    
    examiner_id: IDType
    event_id: IDType

    id: IDType
    lastchange: datetime.datetime
    created: datetime.datetime

    semester: SemesterInputFilter
    student: StudentInputFilter
    exam: ExamInputFilter
    # parts: "Eva"


@strawberry.federation.type(
    keys=["id"],
    description="Exam evaluation"
)
class EvaluationGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ClassificationModel
    
    order: typing.Optional[int] = strawberry.field(
        default=None,
        description="index of attempt",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    points: typing.Optional[int] = strawberry.field(
        default=None,
        description="given points for this exam",
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

    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="description given to student and exam",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    classificationlevel_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="given grade / mark id",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    classificationlevel: typing.Optional[ClassificationLevelGQLModel] = strawberry.field(
        description="represents formal mark",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ClassificationLevelGQLModel"](fkey_field_name="classificationlevel_id")
    )

    student_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="id of the student, not user, it is point to relation Program<->User",
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
        description="the event when exam happened and evaluation has been stored",
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

    parts: typing.List["EvaluationGQLModel"] = strawberry.field(
        description="sub parts of this evaluation",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EvaluationGQLModel"](fkey_field_name="parent_id", whereType=EvaluationInputFilter)
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

from uoishelpers.resolvers import TreeInputStructureMixin
@strawberry.input(
    description="parameter for create"
)
class EvaluationInsertGQLModel(TreeInputStructureMixin):
    getLoader = EvaluationGQLModel.getLoader
    def set_rbacobject_id(self, rbacobject_id):
        self.rbacobject_id = rbacobject_id
        for part in self.evaluation.parts:
            part.set_rbacobject_id(rbacobject_id)

    exam_id: typing.Optional[IDType] = strawberry.field(
        description="Exam plan", 
        # default=None
    )

    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value", default=None)
    # semester_id: typing.Optional[IDType] = strawberry.field(description="Which semester / subject is examined", default=None)
    
    order: typing.Optional[int] = strawberry.field(description="index of attempt", default=None)
    points: typing.Optional[int] = strawberry.field(description="given points for this exam", default=None)
    passed: typing.Optional[bool] = strawberry.field(description="True if student passed this exam", default=None)
    description: typing.Optional[str] = strawberry.field(description="description given to student and exam", default=None)
    classificationlevel_id: typing.Optional[IDType] = strawberry.field(description="Formal given grade", default=None)
    event_id: typing.Optional[IDType] = strawberry.field(description="the event when exam happened and evaluation has been stored", default=None)
    parent_id: typing.Optional[IDType] = strawberry.field(description="id of exam which this is part", default=None)
    student_id: typing.Optional[IDType] = strawberry.field(description="id of the student, not user, it points to relation of Program and User", default=None)
    examiner_id: typing.Optional[IDType] = strawberry.field(description="who examined", default=None)
    
    parts: typing.Optional[typing.List["EvaluationInsertGQLModel"]] = strawberry.field(description="parts of the evaluation", default_factory=list)

    # Private pole – bez použití strawberry.field
    path: strawberry.Private[str] = ""
    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="parameter for update"
)
class EvaluationUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the evaluation to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    semester_id: typing.Optional[IDType] = strawberry.field(description="Which semester / subject is examined", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="Who is examined", default=None)
    order: typing.Optional[int] = strawberry.field(description="index of attempt", default=None)
    points: typing.Optional[int] = strawberry.field(description="given points for this exam", default=None)
    passed: typing.Optional[bool] = strawberry.field(description="True if student passed this exam", default=None)
    description: typing.Optional[str] = strawberry.field(description="description given to student and exam", default=None)
    grade: typing.Optional[str] = strawberry.field(description="given grade / mark", default=None)
    classificationlevel_id: typing.Optional[IDType] = strawberry.field(description="Formal given grade", default=None)
    exam_id: typing.Optional[IDType] = strawberry.field(description="Exam plan", default=None)
    event_id: typing.Optional[IDType] = strawberry.field(description="the event when exam happened and evaluation has been stored", default=None)
    # parent_id: typing.Optional[IDType] = strawberry.field(description="id of exam which this is part", default=None)
    # student_id: typing.Optional[IDType] = strawberry.field(description="id of the student", default=None)
    examiner_id: typing.Optional[IDType] = strawberry.field(description="who examined", default=None)
    exam_id: typing.Optional[IDType] = strawberry.field(description="related exam conditions", default=None)

@strawberry.input(
    description="parameter for delete"
)
class EvaluationDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the evaluation to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

from .StudyPlanGQLModel import StudyPlanGQLModel
@strawberry.interface(
    description=""
)
class EvaluationMutation:
    @strawberry.mutation(
        description="inserts a new evaluation",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            # UserAbsoluteAccessControlExtension[InsertError, EvaluationGQLModel](roles=[
            #     "administrátor",
            #     "studijní administrátor"
            # ]),
            UserAccessControlExtension[InsertError, EvaluationGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                    "zkoušející"
                ]
            ),
            UserRoleProviderExtension[InsertError, EvaluationGQLModel](),
            RbacProviderExtension[InsertError, EvaluationGQLModel](),
            LoadDataExtension[InsertError, EvaluationGQLModel](
                primary_key_name="semester_id", 
                getLoader=StudyPlanGQLModel.getLoader
            )
        ],
    )
    async def evaluation_insert(
        self, 
        info: strawberry.types.Info, 
        evaluation: EvaluationInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[EvaluationGQLModel, InsertError[EvaluationGQLModel]]:
        evaluation.set_rbacobject_id(rbacobject_id)
        result = await Insert[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result
    
    @strawberry.mutation(
        description="updates an existing evaluation",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            # UserAbsoluteAccessControlExtension[InsertError, EvaluationGQLModel](roles=[
            #     "administrátor",
            #     "studijní administrátor"
            # ]),
            UserAccessControlExtension[UpdateError, EvaluationGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu"
                ]
            ),
            UserRoleProviderExtension[UpdateError, EvaluationGQLModel](),
            RbacProviderExtension[UpdateError, EvaluationGQLModel](),
            LoadDataExtension[UpdateError, EvaluationGQLModel]()
        ],
    )
    async def evaluation_update(
        self, 
        info: strawberry.types.Info, 
        evaluation: EvaluationUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[EvaluationGQLModel, UpdateError[EvaluationGQLModel]]:
        
        result = await Update[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result

    @strawberry.mutation(
        description="deletes an existing evaluation",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAbsoluteAccessControlExtension[InsertError, EvaluationGQLModel](roles=[
                "studijní administrátor", 
                # "studijní administrátor"
            ]),
            # UserAccessControlExtension[DeleteError, EvaluationGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, EvaluationGQLModel](),
            RbacProviderExtension[DeleteError, EvaluationGQLModel](),
            LoadDataExtension[DeleteError, EvaluationGQLModel]()
        ],
    )
    async def evaluation_delete(
        self, 
        info: strawberry.types.Info, 
        evaluation: EvaluationUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[EvaluationGQLModel]]:
        result = await Delete[EvaluationGQLModel].DoItSafeWay(info=info, entity=evaluation)
        return result

