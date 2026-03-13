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

ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy(".ProgramGQLModel")]
SemesterGQLModel = typing.Annotated["SemesterGQLModel", strawberry.lazy(".SemesterGQLModel")]
SemesterInputFilter = typing.Annotated["SemesterInputFilter", strawberry.lazy(".SemesterGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("..GroupGQLModel")]

@createInputs
@dataclasses.dataclass
class SubjectInputFilter:
    id: IDType
    name: str

@strawberry.federation.type(    
    keys=["id"], 
    description="""Subject entity"""
    )
class SubjectGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).SubjectModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="subject name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="subject name in english", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description: typing.Optional[str] = strawberry.field(
        default=None,
        description="subject description", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="subject description in english", 
        permission_classes=[OnlyForAuthentized]
        )
    
    program_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="program id", 
        permission_classes=[OnlyForAuthentized]
        )
    
    program: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="program entity", 
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["ProgramGQLModel"](fkey_field_name="program_id")
        )
    
    semesters: typing.List["SemesterGQLModel"] = strawberry.field(
        description="subject semesters", 
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["SemesterGQLModel"](fkey_field_name="subject_id", whereType=SemesterInputFilter)
        )
    
    guarantors_group_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="guarantors of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    guarantors: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="guarantors of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="guarantors_group_id")
    )


@strawberry.interface(
    description=""
)
class SubjectQuery:
    subject_by_id: typing.Optional["SubjectGQLModel"] = strawberry.field(
        description="returns subject by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=SubjectGQLModel.load_with_loader
    )

    subject_page: typing.List["SubjectGQLModel"] = strawberry.field(
        description="returns subjects defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["SubjectGQLModel"](whereType=SubjectInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class SubjectInsertGQLModel(InputModelMixin):
    getLoader = SubjectGQLModel.getLoader
    # rbacobject_id: typing.Optional[IDType] = strawberry.field(
    #     description="rbac proxy object, usually specially created RBACObjectGQLModel"
    # )
    program_id: IDType = strawberry.field(
        description="program id", 
        default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="primary key client generated", 
        default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="subject name", 
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="subject name in english", 
        default=None
    )
    description: typing.Optional[str] = strawberry.field(
        description="subject description", 
        default=None
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="subject description in english", 
        default=None
    )
    group_id: typing.Optional[IDType] = strawberry.field(
        description="guarantors of subject", 
        default=None
    )
    from .SemesterGQLModel import SemesterInsertGQLModel
    semesters: typing.Optional[typing.List[SemesterInsertGQLModel]] = strawberry.field(
        description="semesters of subject",
        default_factory=list,
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class SubjectUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="subject name", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="subject name in english", default=None)
    description: typing.Optional[str] = strawberry.field(description="subject description", default=None)
    description_en: typing.Optional[str] = strawberry.field(description="subject description in english", default=None)
    # program_id: typing.Optional[IDType] = strawberry.field(description="program id", default=None)
    # group_id: typing.Optional[IDType] = strawberry.field(description="guarantors of programme", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class SubjectDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description="Mutations for SubjectGQLModel"
)
class SubjectMutation:
    from .ProgramGQLModel import ProgramGQLModel
    @strawberry.mutation(
        description="create a new subject",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, SubjectGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[InsertError, SubjectGQLModel](),
            RbacProviderExtension[InsertError, SubjectGQLModel](),
            LoadDataExtension[InsertError, SubjectGQLModel](
                primary_key_name="program_id",
                getLoader=ProgramGQLModel.getLoader
            )
        ]
    )
    async def subject_insert(
        self, 
        info: strawberry.types.Info, 
        subject: SubjectInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[SubjectGQLModel, InsertError[SubjectGQLModel]]:
        subject.rbacobject_id = rbacobject_id
        return await Insert[SubjectGQLModel].DoItSafeWay(info=info, entity=subject)
        
    
    @strawberry.mutation(
        description="updates existing subject",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, SubjectGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[UpdateError, SubjectGQLModel](),
            RbacProviderExtension[UpdateError, SubjectGQLModel](),
            LoadDataExtension[UpdateError, SubjectGQLModel]()
        ]
    )
    async def subject_update(
        self, 
        info: strawberry.types.Info, 
        subject: SubjectUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[SubjectGQLModel, UpdateError[SubjectGQLModel]]:
        return await Update[SubjectGQLModel].DoItSafeWay(info=info, entity=subject)
        

    @strawberry.mutation(
        description="delete existing subject",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, SubjectGQLModel](
                roles=[
                    "studijní administrátor", 
                    "garant předmětu",
                    "garant programu",
                ]
            ),
            UserRoleProviderExtension[DeleteError, SubjectGQLModel](),
            RbacProviderExtension[DeleteError, SubjectGQLModel](),
            LoadDataExtension[DeleteError, SubjectGQLModel]()
        ]
    )
    async def subject_delete(
        self, 
        info: strawberry.types.Info, 
        subject: SubjectDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[SubjectGQLModel]]:
        return await Delete[SubjectGQLModel].DoItSafeWay(info=info, entity=subject)


