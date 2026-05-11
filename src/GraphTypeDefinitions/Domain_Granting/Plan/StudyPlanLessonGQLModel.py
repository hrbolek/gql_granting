import logging
import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.file_uploads
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
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType

TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy("..Program.TopicGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_UG.UserGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_UG.GroupGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_Office.FacilityGQLModel")]
EventGQLModel = typing.Annotated["EventGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_Office.EventGQLModel")]
StudyPlanGQLModel = typing.Annotated["StudyPlanGQLModel", strawberry.lazy(".StudyPlanGQLModel")]
LessonTypeGQLModel = typing.Annotated["LessonTypeGQLModel", strawberry.lazy("..Program.LessonTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class StudyPlanLessonInputFilter:
    id: IDType
    name: str
    order: int
    length: int
    event_id: IDType
    topic_id: IDType
    linked_with_id: IDType

@strawberry.federation.type(
    keys=["id"],
    description="On row in studyplan"
)
class StudyPlanLessonGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).PlanItemModel

    order: typing.Optional[int] = strawberry.field(
        description="order in plan",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name: typing.Optional[str] = strawberry.field(
        description="lesson name",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="lesson name in english",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    length: typing.Optional[int] = strawberry.field(
        description="length in fictive units",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    event_id: typing.Optional[IDType] = strawberry.field(
        description="id of event which has been planed for this lesson",
        default=None,
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
        default=None,
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

    lessontype_id: typing.Optional[IDType] = strawberry.field(
        description="Lesson type",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    lessontype: typing.Optional[LessonTypeGQLModel] = strawberry.field(
        description="type of the lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[LessonTypeGQLModel](fkey_field_name="lessontype_id")
    )

    linked_with_id: typing.Optional[IDType] = strawberry.field(
        description="key to describe integration with other planned lessons",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ],
    )

    plan_id: typing.Optional[IDType] = strawberry.field(
        description="Plan which owns this lesson",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    plan: typing.Optional[StudyPlanGQLModel] = strawberry.field(
        description="the plan to which this lesson belongs",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StudyPlanGQLModel](fkey_field_name="plan_id")
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
        from src.GraphTypeDefinitions.Domain_UG.UserGQLModel import UserGQLModel
        loader = getLoadersFromInfo(info).PlanItemTeacherModel
        rows = await loader.filter_by(planitem_id=self.id)
        rows = [row for row in rows]
        ruid = [{"uid": row.user_id, "id": row.id} for row in rows]
        print(ruid)
        valid = [row for row in rows if row.user_id is not None]
        return [UserGQLModel.resolve_reference(info=info, id=row.user_id) for row in valid]

    @strawberry.field(
        description="study groups",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def study_groups(self, info: strawberry.types.Info) -> typing.List["GroupGQLModel"]:
        from src.GraphTypeDefinitions.Domain_UG.GroupGQLModel import GroupGQLModel
        loader = getLoadersFromInfo(info).PlanItemGroupModel
        rows = await loader.filter_by(planitem_id=self.id)
        valid = [row for row in rows if row.group_id is not None]
        return [GroupGQLModel(id=row.group_id) for row in valid]
    
    @strawberry.field(
        description="places for this lesson",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def facilities(self, info: strawberry.types.Info) -> typing.List["FacilityGQLModel"]:
        from src.GraphTypeDefinitions.Domain_Office.FacilityGQLModel import FacilityGQLModel
        loader = getLoadersFromInfo(info).PlanItemFacilityModel
        rows = await loader.filter_by(planitem_id=self.id)
        valid = [row for row in rows if row.facility_id is not None]
        return [FacilityGQLModel(id=row.facility_id) for row in valid]
    

@strawberry.interface()
class StudyPlanLessonQuery:
    study_plan_lesson_by_id: typing.Optional[StudyPlanLessonGQLModel] = strawberry.field(
        description="study plan lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=StudyPlanLessonGQLModel.load_with_loader
    )

    study_plan_lesson_page: typing.List[StudyPlanLessonGQLModel] = strawberry.field(
        description="filtered list of study plan lessons",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[StudyPlanLessonGQLModel](whereType=StudyPlanLessonInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin

@strawberry.input(
    description="parameter for create"
)
class StudyPlanLessonInsertGQLModel(InputModelMixin):
    getLoader = StudyPlanLessonGQLModel.getLoader
    plan_id: IDType = strawberry.field(
        description="The identifier of the study plan that this lesson belongs to.", default=None
    )
    lessontype_id: IDType = strawberry.field(
        description="The identifier of the lesson type (e.g. lecture, seminar, lab) for this study plan lesson.", default=None
    )
    topic_id: IDType = strawberry.field(
        description="The identifier of the topic associated with this study plan lesson.", default=None
    )
    event_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier of an event linked to this study plan lesson (if applicable).", default=None
    )
    linked_with_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier of another study plan lesson that this study plan lesson is linked with (e.g. a follow-up or complementary session).", default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the study plan lesson.", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the study plan lesson.", default=None
    )
    length: typing.Optional[int] = strawberry.field(
        description="The duration or length of the study plan lesson, expressed in virtual units.", default=None
    )
    order: typing.Optional[int] = strawberry.field(
        description="order in plan",
        default=None
    )  
    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value", default=None)

    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private["IDType"] = None    



@strawberry.input(
    description="parameter for update"
)
class StudyPlanLessonUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the study_plan_lesson to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

    lessontype_id: typing.Optional[IDType] = strawberry.field(
        description="The identifier of the lesson type (e.g. lecture, seminar, lab) for this study plan lesson.", default=strawberry.UNSET
    )
    topic_id: typing.Optional[IDType] = strawberry.field(
        description="The identifier of the topic associated with this study plan lesson.", default=strawberry.UNSET
    )
    event_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier of an event linked to this study plan lesson (if applicable).", default=strawberry.UNSET
    )
    linked_with_id: typing.Optional[IDType] = strawberry.field(
        description="Optional identifier of another study plan lesson that this study plan lesson is linked with (e.g. a follow-up or complementary session).", default=strawberry.UNSET
    )
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the study plan lesson.", default=strawberry.UNSET
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the study plan lesson.", default=strawberry.UNSET
    )
    length: typing.Optional[int] = strawberry.field(
        description="The duration or length of the study plan lesson, expressed in virtual units.", default=strawberry.UNSET
    )
    order: typing.Optional[int] = strawberry.field(
        description="order in plan",
        default=strawberry.UNSET
    )  
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for delete"
)
class StudyPlanLessonDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the study_plan_lesson to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.input(
    description="parameter for adding or removing the instructor from lesson plan"
)
class StudyPlanLessonAddRemoveInstructor:
    planitem_id: IDType = strawberry.field(description="study plan primary key")
    user_id: IDType = strawberry.field(description="instructor primary key")
    

@strawberry.input(
    description="parameter for adding or removing the facility from lesson plan"
)
class StudyPlanLessonAddRemoveFacility:
    planitem_id: IDType = strawberry.field(description="study plan primary key")
    facility_id: IDType = strawberry.field(description="facility primary key")

@strawberry.input(
    description="parameter for adding or removing the study group from lesson plan"
)
class StudyPlanLessonAddRemoveStudyGroup:
    planitem_id: IDType = strawberry.field(description="study plan primary key")
    group_id: IDType = strawberry.field(description="group primary key")

@strawberry.interface(
    description=""
)
class StudyPlanLessonMutation:
    from .StudyPlanGQLModel import StudyPlanGQLModel
    @strawberry.mutation(
        description="inserts a new study_plan_lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](
                primary_key_name="plan_id",
                getLoader=StudyPlanGQLModel.getLoader
            )
        ]
    )
    async def study_plan_lesson_insert(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, InsertError[StudyPlanLessonGQLModel]]:
        study_plan_lesson.rbacobject_id = db_row.rbacobject_id
        result = await Insert[StudyPlanLessonGQLModel].DoItSafeWay(info=info, entity=study_plan_lesson)
        return result
    
    @strawberry.mutation(
        description="updates an existing evaluatio",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel]()
        ]
    )
    async def study_plan_lesson_update(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        result = await Update[StudyPlanLessonGQLModel].DoItSafeWay(info=info, entity=study_plan_lesson)
        return result

    @strawberry.mutation(
        description="deletes an existing study_plan_lesson",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[DeleteError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[DeleteError, StudyPlanLessonGQLModel](),
            LoadDataExtension[DeleteError, StudyPlanLessonGQLModel]()
        ]
    )
    async def study_plan_lesson_delete(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[StudyPlanLessonGQLModel]]:
        result = await Delete[StudyPlanLessonGQLModel].DoItSafeWay(info=info, entity=study_plan_lesson)
        return result

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
            # LoadDataExtension[UpdateError, StudyPlanLessonGQLModel]()
        ]
    )
    async def study_plan_lesson_add_instructor(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveInstructor,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        # studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        # logging.info(f"study_plan_lesson_add_instructor: {self}")
        studyplanlesson = StudyPlanLessonGQLModel.from_dataclass(db_row) if db_row else None
        # logging.info(f"study_plan_lesson_add_instructor.studyplanlesson: {studyplanlesson}")
        loader = getLoadersFromInfo(info).PlanItemTeacherModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, user_id=study_plan_lesson.user_id)
        row = next(iter(rows), None)
        # logging.info(f"study_plan_lesson_add_instructor.row: {row}")
        if row:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Instructor is already planned for this study plan item",
                code="1f7fe358-c83b-4ecb-8aeb-a042b139356e",
                _input=study_plan_lesson
                )
        try:
            await loader.insert(study_plan_lesson)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
        ]
    )
    async def study_plan_lesson_remove_instructor(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveInstructor,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        # studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        studyplanlesson = StudyPlanLessonGQLModel.from_dataclass(db_row) if db_row else None
        loader = getLoadersFromInfo(info).PlanItemTeacherModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, user_id=study_plan_lesson.user_id)
        row = next(iter(rows), None)
        if row is None:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Instructor is not planned for this study plan item",
                code="a8b820e1-2659-4605-94ba-4373900dd98f",
                _input=study_plan_lesson
                )
        try:
            await loader.delete(row.id)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
        ]
    )
    async def study_plan_lesson_add_facility(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveFacility,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        # studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        studyplanlesson = StudyPlanLessonGQLModel.from_dataclass(db_row) if db_row else None
        loader = getLoadersFromInfo(info).PlanItemFacilityModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, facility_id=study_plan_lesson.facility_id)
        row = next(iter(rows), None)
        if row:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Facility is already planned for this study plan item",
                code="36983127-5d52-4bd5-b4ee-5c01665589ba",
                _input=study_plan_lesson
                )
        try:
            await loader.insert(study_plan_lesson)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
        ]
    )
    async def study_plan_lesson_remove_facility(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveFacility,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        # studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        studyplanlesson = StudyPlanLessonGQLModel.from_dataclass(db_row) if db_row else None
        
        loader = getLoadersFromInfo(info).PlanItemFacilityModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, facility_id=study_plan_lesson.facility_id)
        row = next(iter(rows), None)
        if row is None:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Facility is not planned for this study plan item",
                code="b69dde53-4c7f-4909-8025-1874165db8d8",
                _input=study_plan_lesson
                )
        try:
            await loader.delete(row.id)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
        ]
    )
    async def study_plan_lesson_add_group(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveStudyGroup,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        loader = getLoadersFromInfo(info).PlanItemGroupModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, group_id=study_plan_lesson.group_id)
        row = next(iter(rows), None)
        if row:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Group is already planned for this study plan item",
                code="f866f8ed-a47e-4c6a-8e29-e68e22ebb1a5",
                _input=study_plan_lesson
                )
        try:
            await loader.insert(study_plan_lesson)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

    @strawberry.mutation(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudyPlanLessonGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            RbacProviderExtension[UpdateError, StudyPlanLessonGQLModel](),
            LoadDataExtension[UpdateError, StudyPlanLessonGQLModel](primary_key_name="planitem_id")
        ]
    )
    async def study_plan_lesson_remove_group(
        self, 
        info: strawberry.types.Info, 
        study_plan_lesson: StudyPlanLessonAddRemoveStudyGroup,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudyPlanLessonGQLModel, UpdateError[StudyPlanLessonGQLModel]]:
        studyplanlesson = await StudyPlanLessonGQLModel.load_with_loader(info, id=study_plan_lesson.planitem_id)
        loader = getLoadersFromInfo(info).PlanItemGroupModel
        rows = await loader.filter_by(planitem_id=study_plan_lesson.planitem_id, group_id=study_plan_lesson.group_id)
        row = next(iter(rows), None)
        if row is None:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg="Group is not planned for this study plan item",
                code="4d7798dc-24e4-4d37-886b-7f1dda701fd0",
                _input=study_plan_lesson
                )
        try:
            await loader.delete(row.id)
        except Exception as e:
            return UpdateError[StudyPlanLessonGQLModel](
                _entity=studyplanlesson,
                msg=f"{e}",
                _input=study_plan_lesson
                )
        return studyplanlesson

