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

@strawberry.federation.type(
    keys=["id"],
    description=""
)
class StudentGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info=info).ProgramStudentModel

    student_id: typing.Optional[IDType] = strawberry.field(
        description="id of the user",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    student: typing.Optional["UserGQLModel"] = strawberry.field(
        description="who is student",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["UserGQLModel"](fkey_field_name="student_id")
    )

    program_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    program: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="which program student is studying",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProgramGQLModel"](fkey_field_name="program_id")
    )

    state_id: typing.Optional[IDType] = strawberry.field(
        description="",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    semester: typing.Optional[int] = strawberry.field(
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
    )


@strawberry.type(description="")
class StudentQuery:

    @strawberry.field(description="")
    async def hello() -> str:
        return "hello"
