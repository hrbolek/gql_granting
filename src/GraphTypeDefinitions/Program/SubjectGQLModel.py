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

    name: str = strawberry.field(
        description="subject name", 
        permission_classes=[OnlyForAuthentized]
        )
    
    name_en: str = strawberry.field(
        description="subject name in english", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description: str = strawberry.field(
        description="subject description", 
        permission_classes=[OnlyForAuthentized]
        )
    
    description_en: str = strawberry.field(
        description="subject description in english", 
        permission_classes=[OnlyForAuthentized]
        )
    
    program_id: IDType = strawberry.field(
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
    
    guarantors_id: typing.Optional[IDType] = strawberry.field(
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
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="guarantors_id")
    )

