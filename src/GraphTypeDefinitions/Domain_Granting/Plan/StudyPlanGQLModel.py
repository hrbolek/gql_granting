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

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType

SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy("..Program.SemesterGQLModel")]
StudyPlanLessonGQLModel = typing.Annotated["StudyPlanLessonGQLModel", strawberry.lazy(".StudyPlanLessonGQLModel")]
StudyPlanLessonInputFilter = typing.Annotated["StudyPlanLessonInputFilter", strawberry.lazy(".StudyPlanLessonGQLModel")]

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
# ExamInputFilter = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_Office.EventGQLModel")]

@createInputs2
class StudyPlanInputFilter:
    id: IDType
    semester_id: IDType
    exam_id: IDType
    event_id: IDType


@strawberry.federation.type(
    keys=["id"],
    description="set of lessons / events in the specified semester"
)
class StudyPlanGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).PlanModel
    
    semester_id: typing.Optional[IDType] = strawberry.field(
        description="ID of Semester to which the plan is related",
        default=None,
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

    exam_id: typing.Optional[IDType] = strawberry.field(
        description="ID of classification conditions",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    lessons: typing.List["StudyPlanLessonGQLModel"] = strawberry.field(
        description="part of study plan",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudyPlanLessonGQLModel"](fkey_field_name="plan_id", whereType=StudyPlanLessonInputFilter)
    )

    exam: typing.Optional["ExamGQLModel"] = strawberry.field(
        description="Exam Rules",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ExamGQLModel"](fkey_field_name="exam_id")
    )

    event_id: typing.Optional[IDType] = strawberry.field(
        description="Time period when the plan will live",
        default=None,
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
    study_plan_by_id: typing.Optional[StudyPlanGQLModel] = strawberry.field(
        description="study plan",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=StudyPlanGQLModel.load_with_loader
    )

    study_plan_page: typing.List[StudyPlanGQLModel] = strawberry.field(
        description="filtered list of study plan",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[StudyPlanGQLModel](whereType=StudyPlanInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create"
)
class StudyPlanInsertGQLModel(InputModelMixin):
    getLoader = StudyPlanGQLModel.getLoader
    semester_id: IDType = strawberry.field(
        description="Semester to which the plan is linked.",
        # default=None
    )
    event_id: IDType = strawberry.field(
        description="Time period when the plan will live", 
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="optional client generated primary key value", 
        default=None
    )
    exam_id: typing.Optional[IDType] = strawberry.field(description="Exam Rules", default=None)
    
    from .StudyPlanLessonGQLModel import StudyPlanLessonInsertGQLModel
    lessons: typing.Optional[typing.List[StudyPlanLessonInsertGQLModel]] = strawberry.field(
        description="part of study plan",
        default_factory=list
    )  
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private["IDType"] = None    



@strawberry.input(
    description="parameter for update"
)
class StudyPlanUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the studyplan to update", default=None)
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update", default=None)
    # semester_id: typing.Optional[IDType] = strawberry.field(description="Semester to which teh plan is linked.", default=None)
    exam_id: typing.Optional[IDType] = strawberry.field(description="Exam Rules", default=None)
    event_id: typing.Optional[IDType] = strawberry.field(description="Time period when the plan will live", default=None)

@strawberry.input(
    description="parameter for delete"
)
class StudyPlanDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the studyplan to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class StudyPlanMutation:
    from ..Program.SemesterGQLModel import SemesterGQLModel
    @strawberry.mutation(
        description="inserts a new studyplan",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, StudyPlanGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[InsertError, StudyPlanGQLModel](),
            RbacProviderExtension[InsertError, StudyPlanGQLModel](),
            LoadDataExtension[InsertError, StudyPlanGQLModel](
                primary_key_name="semester_id",
                getLoader=SemesterGQLModel.getLoader
            )
        ]
    )
    async def study_plan_insert(
        self, 
        info: strawberry.types.Info, 
        study_plan: StudyPlanInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanGQLModel, InsertError[StudyPlanGQLModel]]:
        study_plan.rbacobject_id = rbacobject_id
        result = await Insert[StudyPlanGQLModel].DoItSafeWay(info=info, entity=study_plan)
        return result
    
    @strawberry.mutation(
        description="updates an existing studyplan",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanGQLModel]()
        ]
    )
    async def study_plan_update(
        self, 
        info: strawberry.types.Info, 
        study_plan: StudyPlanUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanGQLModel, UpdateError[StudyPlanGQLModel]]:
        result = await Update[StudyPlanGQLModel].DoItSafeWay(info=info, entity=study_plan)
        return result

    @strawberry.mutation(
        description="deletes an existing studyplan",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, StudyPlanGQLModel](roles=[
                "studijní administrátor", 
                "garant programu",
            ]),
            UserRoleProviderExtension[DeleteError, StudyPlanGQLModel](),
            RbacProviderExtension[DeleteError, StudyPlanGQLModel](),
            LoadDataExtension[DeleteError, StudyPlanGQLModel]()
        ]
    )
    async def study_plan_delete(
        self, 
        info: strawberry.types.Info, 
        study_plan: StudyPlanUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[StudyPlanGQLModel]]:
        result = await Delete[StudyPlanGQLModel].DoItSafeWay(info=info, entity=study_plan)
        return result

