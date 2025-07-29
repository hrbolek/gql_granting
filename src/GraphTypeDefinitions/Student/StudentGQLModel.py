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

from ..BaseGQLModel import BaseGQLModel, IDType, Relation

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("..UserGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("..StateGQLModel")]
ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy("..Program.ProgramGQLModel")]
EvaluationGQLModel = typing.Annotated["EvaluationGQLModel", strawberry.lazy("..Plan.EvaluationGQLModel")]
EvaluationInputFilter = typing.Annotated["EvaluationInputFilter", strawberry.lazy("..Plan.EvaluationGQLModel")]


@createInputs
@dataclasses.dataclass
class StudentInputFilter:
    id: IDType
    user_id: IDType
    program_id: IDType
    semester_number: int
    state_id: IDType

@strawberry.federation.type(
    keys=["id"],
    description="Connects an user with a program to define that somebody is studying a program."
)
class StudentGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ProgramStudentModel

    user_id: typing.Optional[IDType] = strawberry.field(
        description="id of the user",
        permission_classes=[
            OnlyForAuthentized
        ],
        directives=[
            Relation(to="UserGQLModel")
        ],
        default=None
    )

    user: typing.Optional["UserGQLModel"] = strawberry.field(
        description="who is student",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["UserGQLModel"](fkey_field_name="user_id")
    )

    program_id: typing.Optional[IDType] = strawberry.field(
        description="the program which user is studying",
        permission_classes=[
            OnlyForAuthentized
        ],
        directives=[
            Relation(to="ProgramGQLModel")
        ],
        default=None
    )

    program: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="which program student is studying",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProgramGQLModel"](fkey_field_name="program_id")
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="in what state the student is",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    semester_number: typing.Optional[int] = strawberry.field(
        default=None,
        description="semester of study",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    state: typing.Optional["StateGQLModel"] = strawberry.field(
        description="State of the user study",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )

    evaluations: typing.List["EvaluationGQLModel"] = strawberry.field(
        description="given grades",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["EvaluationGQLModel"](fkey_field_name="student_id", whereType=EvaluationInputFilter)
        # resolver=lambda self: []
    )


@strawberry.interface(
    description=""
)
class StudentQuery:
    student_by_id: typing.Optional["StudentGQLModel"] = strawberry.field(
        description="returns student by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=StudentGQLModel.load_with_loader
    )

    student_page: typing.List["StudentGQLModel"] = strawberry.field(
        description="returns students defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["StudentGQLModel"](whereType=StudentInputFilter)
    )

@strawberry.input(
    description="parameter for create operation"
)
class StudentInsertGQLModel:
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="id of the user")
    program_id: typing.Optional[IDType] = strawberry.field(description="id of the program")
    state_id: typing.Optional[IDType] = strawberry.field(description="id of the state")
    semester_number: typing.Optional[int] = strawberry.field(description="semester of study", default=None)

@strawberry.input(
    description="parameter for update operation"
)
class StudentUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    user_id: typing.Optional[IDType] = strawberry.field(description="id of the user", default=None)
    program_id: typing.Optional[IDType] = strawberry.field(description="id of the program", default=None)
    state_id: typing.Optional[IDType] = strawberry.field(description="id of the state", default=None)
    semester_number: typing.Optional[int] = strawberry.field(description="semester of study", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class StudentDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class StudentMutation:

    @strawberry.mutation(
        description="create a new student",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, StudentGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, StudentGQLModel](),
            RbacProviderExtension[InsertError, StudentGQLModel](),
            LoadDataExtension[InsertError, StudentGQLModel]()
        ]
    )
    async def student_insert(
        self, 
        info: strawberry.types.Info, 
        student: StudentInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudentGQLModel, InsertError[StudentGQLModel]]:
        result = await Insert[StudentGQLModel].DoItSafeWay(info=info, entity=student)
        return result
    
    @strawberry.mutation(
        description="updates existing student",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudentGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[UpdateError, StudentGQLModel](),
            RbacProviderExtension[UpdateError, StudentGQLModel](),
            LoadDataExtension[UpdateError, StudentGQLModel]()
        ]
    )
    async def student_update(
        self, 
        info: strawberry.types.Info, 
        student: StudentUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudentGQLModel, UpdateError[StudentGQLModel]]:
        result = await Update[StudentGQLModel].DoItSafeWay(info=info, entity=student)
        return result

    @strawberry.mutation(
        description="delete existing student",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, StudentGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, StudentGQLModel](),
            RbacProviderExtension[DeleteError, StudentGQLModel](),
            LoadDataExtension[DeleteError, StudentGQLModel]()
        ]
    )
    async def student_delete(
        self, 
        info: strawberry.types.Info,
        student: StudentDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[StudentGQLModel]]:
        result = await Delete[StudentGQLModel].DoItSafeWay(info=info, entity=student)
        return result

