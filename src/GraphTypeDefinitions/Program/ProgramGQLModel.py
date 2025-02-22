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

SubjectGQLModel = typing.Annotated["SubjectGQLModel", strawberry.lazy(".SubjectGQLModel")]
SubjectInputFilter = typing.Annotated["SubjectInputFilter", strawberry.lazy(".SubjectGQLModel")]
StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy("..Student.StudentGQLModel")]
StudentInputFilter = typing.Annotated["StudentInputFilter", strawberry.lazy("..Student.StudentGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("..GroupGQLModel")]
ProgramTypeGQLModel = typing.Annotated["ProgramTypeGQLModel", strawberry.lazy(".ProgramTypeGQLModel")]

@createInputs
@dataclasses.dataclass
class ProgramInputFilter:
    id: IDType
    name: str


@strawberry.federation.type(
    keys=["id"],
    description="""Program entity, represents an accredited study""")
class ProgramGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ProgramModel
    
    name: typing.Optional[str] = strawberry.field(
        description="Name of program",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="Eng. name of program",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    subjects: typing.List["SubjectGQLModel"] = strawberry.field(
        description="""Program subjects""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["SubjectGQLModel"](fkey_field_name="program_id", whereType=SubjectInputFilter)
    )

    students: typing.List["StudentGQLModel"] = strawberry.field(
        description="students",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudentGQLModel"](fkey_field_name="program_id", whereType=StudentInputFilter)
    )

    group_id: typing.Optional[IDType] = strawberry.field(
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
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="group_id")
    )

    licenced_group_id: typing.Optional[IDType] = strawberry.field(
        description="Who has got license for programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    licenced_group: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="Who has got license for programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="licenced_group_id")
    )    

    type_id: typing.Optional[IDType] = strawberry.field(
        description="type of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    type_: typing.Optional["ProgramTypeGQLModel"] = strawberry.field(
        name="type",
        description="type of pragramme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProgramTypeGQLModel"](fkey_field_name="type_id")
    )

@strawberry.interface(
    description=""
)
class ProgramQuery:
    program_by_id: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="returns program by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramGQLModel.load_with_loader
    )

    program_page: typing.List["ProgramGQLModel"] = strawberry.field(
        description="returns programs defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramGQLModel"](whereType=ProgramInputFilter)
    )

@strawberry.input(
    description="parameter for create operation"
)
class ProgramInsertGQLModel:
    name: str = strawberry.field(
        description="name of the program"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class ProgramUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramMutation:

    @strawberry.mutation(
        description="create a new program"
    )
    async def program_insert(self, info: strawberry.types.Info, program: ProgramInsertGQLModel) -> typing.Union[ProgramGQLModel, InsertError[ProgramGQLModel]]:
        result = await Insert[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        return result
    
    @strawberry.mutation(
        description="updates existing program",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_update(self, info: strawberry.types.Info, program: ProgramUpdateGQLModel) -> typing.Union[ProgramGQLModel, UpdateError[ProgramGQLModel]]:
        result = await Update[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        return result

    @strawberry.mutation(
        description="delete existing program",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def program_delete(self, info: strawberry.types.Info, program: ProgramDeleteGQLModel) -> typing.Optional[DeleteError[ProgramGQLModel]]:
        result = await Delete[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        return result

