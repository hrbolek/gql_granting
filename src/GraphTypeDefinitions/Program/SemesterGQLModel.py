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
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

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
        default=None,
        description="order in same subject", 
        permission_classes=[OnlyForAuthentized]
    )

    mandatory: typing.Optional[bool] = strawberry.field(
        default=None,
        description="True if every student must pass this subject", 
        permission_classes=[OnlyForAuthentized]
    )

    credits: typing.Optional[int] = strawberry.field(
        default=None,
        description="credits", 
        permission_classes=[OnlyForAuthentized]
    )

    classificationtype_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="subject id", 
        permission_classes=[OnlyForAuthentized]
    )

    subject_id: typing.Optional[IDType] = strawberry.field(
        default=None,
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
        permission_classes=[OnlyForAuthentized],
        resolver=lambda: []
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


@strawberry.interface(
    description=""
)
class SemesterQuery:
    semester_by_id: typing.Optional["SemesterGQLModel"] = strawberry.field(
        description="returns semester by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=SemesterGQLModel.load_with_loader
    )

    semester_page: typing.List["SemesterGQLModel"] = strawberry.field(
        description="returns semesters defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["SemesterGQLModel"](whereType=SemesterInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class SemesterInsertGQLModel(InputModelMixin):
    subject_id: typing.Optional[IDType] = strawberry.field(
        description="subject id", 
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="primary key client generated", default=None)
    order: typing.Optional[int] = strawberry.field(
        description="order in same subject", default=None)
    mandatory: typing.Optional[bool] = strawberry.field(
        description="True if every student must pass this subject", default=None)
    credits: typing.Optional[int] = strawberry.field(
        description="credits", default=None)
    classificationtype_id: typing.Optional[IDType] = strawberry.field(
        description="subject id", default=None)

    from .TopicGQLModel import TopicInsertGQLModel
    topics: typing.Optional[typing.List[TopicInsertGQLModel]] = strawberry.field(
        description="topics of semester",
        default_factory=list,
    )

    rbacobject_id: strawberry.Private[IDType] = None
    changedby_id: strawberry.Private[IDType] = None




@strawberry.input(
    description="parameter for update operation"
)
class SemesterUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    order: typing.Optional[int] = strawberry.field(description="order in same subject", default=None)
    mandatory: typing.Optional[bool] = strawberry.field(description="True if every student must pass this subject", default=None)
    credits: typing.Optional[int] = strawberry.field(description="credits", default=None)
    classificationtype_id: typing.Optional[IDType] = strawberry.field(description="subject id", default=None)
    subject_id: typing.Optional[IDType] = strawberry.field(description="subject id", default=None)
    
@strawberry.input(
    description="parameter for delete operation"
)
class SemesterDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description="Mutations for SemesterGQLModel"
)
class SemesterMutation:
    from .SubjectGQLModel import SubjectGQLModel
    @strawberry.mutation(
        description="create a new semester",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, SemesterGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[InsertError, SemesterGQLModel](),
            RbacProviderExtension[InsertError, SemesterGQLModel](),
            LoadDataExtension[InsertError, SemesterGQLModel](
                primary_key_name="subject_id",
                getLoader=SubjectGQLModel.getLoader
            )
        ]
    )
    async def semester_insert(
        self, 
        info: strawberry.types.Info, 
        semester: SemesterInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[SemesterGQLModel, InsertError[SemesterGQLModel]]:
        semester.rbacobject_id = rbacobject_id
        return await Insert[SemesterGQLModel].DoItSafeWay(info=info, entity=semester)
        
    
    @strawberry.mutation(
        description="updates existing semester",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, SemesterGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, SemesterGQLModel](),
            RbacProviderExtension[UpdateError, SemesterGQLModel](),
            LoadDataExtension[UpdateError, SemesterGQLModel]()
        ]
    )
    async def semester_update(
        self, 
        info: strawberry.types.Info, 
        semester: SemesterUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[SemesterGQLModel, UpdateError[SemesterGQLModel]]:
        return await Update[SemesterGQLModel].DoItSafeWay(info=info, entity=semester)
        

    @strawberry.mutation(
        description="delete existing semester",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, SemesterGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[DeleteError, SemesterGQLModel](),
            RbacProviderExtension[DeleteError, SemesterGQLModel](),
            LoadDataExtension[DeleteError, SemesterGQLModel]()
        ]
    )
    async def semester_delete(
        self, 
        info: strawberry.types.Info, 
        semester: SemesterDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[SemesterGQLModel]]:
        return await Delete[SemesterGQLModel].DoItSafeWay(info=info, entity=semester)
        

