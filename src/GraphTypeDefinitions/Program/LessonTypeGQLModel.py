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
    lesson_type_by_id: typing.Optional["LessonTypeGQLModel"] = strawberry.field(
        description="returns program by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=LessonTypeGQLModel.load_with_loader
    )

    lesson_type_page: typing.List["LessonTypeGQLModel"] = strawberry.field(
        description="returns programs defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["LessonTypeGQLModel"](whereType=LessonTypeInputFilter)
    )


@strawberry.input(
    description="parameter for create"
)
class LessonTypeInsertGQLModel:
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the lesson_type."
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the lesson_type."
    )
    id: typing.Optional[IDType] = strawberry.field(description="optional client generated primary key value")

    semester_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(
    description="parameter for update"
)
class LessonTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="id of the lesson_type to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")
    name: typing.Optional[str] = strawberry.field(
        description="The localized name of the lesson_type."
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the lesson_type."
    )

@strawberry.input(
    description="parameter for delete"
)
class LessonTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="id of the lesson_type to update")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurent update")

@strawberry.interface(
    description=""
)
class LessonTypeMutation:

    @strawberry.mutation(
        description="inserts a new lesson_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def lesson_type_insert(self, info: strawberry.types.Info, lesson_type: LessonTypeInsertGQLModel) -> typing.Union[LessonTypeGQLModel, InsertError[LessonTypeGQLModel]]:
        result = await Insert[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        return result
    
    @strawberry.mutation(
        description="updates an existing evaluatio",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def lesson_type_update(self, info: strawberry.types.Info, lesson_type: LessonTypeUpdateGQLModel) -> typing.Union[LessonTypeGQLModel, UpdateError[LessonTypeGQLModel]]:
        result = await Update[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        return result

    @strawberry.mutation(
        description="deletes an existing lesson_type",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def lesson_type_delete(self, info: strawberry.types.Info, lesson_type: LessonTypeUpdateGQLModel) -> typing.Optional[DeleteError[LessonTypeGQLModel]]:
        result = await Delete[LessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
        return result

