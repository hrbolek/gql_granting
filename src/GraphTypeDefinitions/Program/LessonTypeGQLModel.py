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


TopicGQLModel = typing.Annotated["TopicGQLModel", strawberry.lazy(".TopicGQLModel")]

@createInputs
@dataclasses.dataclass
class LessonTypeInputFilter:
    id: IDType
    name: str
    name_en: str

@strawberry.federation.type(
    keys=["id"],
    description="""LessonType entity"""
    )
class LessonTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).LessonTypeModel

    name: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="english name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )


@strawberry.interface(
    description=""
)
class LessonTypeQuery:
    program_by_id: typing.Optional["LessonTypeGQLModel"] = strawberry.field(
        description="returns program by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=LessonTypeGQLModel.load_with_loader
    )

    program_page: typing.List["LessonTypeGQLModel"] = strawberry.field(
        description="returns programs defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["LessonTypeGQLModel"](whereType=LessonTypeInputFilter)
    )
