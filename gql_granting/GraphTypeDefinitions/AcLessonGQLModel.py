import strawberry
import uuid
import typing
import datetime
import logging
import asyncio
from uuid import UUID
from typing import Optional, List, Union, Annotated

from ..utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from .AcTopicGQLModel import TopicResultGQLModel
from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
#from .AcTopicGQLModel import AcTopicGQLModel

AcTopicGQLModel= Annotated["AcTopicGQLModel",strawberry.lazy(".AcTopicGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents single lesson included in a topic""",
)
class AcLessonGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).lessons
        return loader

    @strawberry.field(description="""primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""datetime lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Lesson type""")
    async def type(self, info: strawberry.types.Info) -> "AcLessonTypeGQLModel":
        result = await AcLessonTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberry.field(description="""Number of hour of this lesson in the topic""")
    def count(self) -> int:
        return self.count

    @strawberry.field(description="""The topic which owns this lesson""")
    async def topic(self, info: strawberry.types.Info) -> Optional["AcTopicGQLModel"]:
        from .AcTopicGQLModel import AcTopicGQLModel
        result = await AcTopicGQLModel.resolve_reference(info, self.topic_id)
        return result

#################################################
# Query
#################################################

@strawberry.field(description="""Finds a lesson by its id""")
async def aclesson_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union["AcLessonGQLModel", None]:
        result = await AcLessonGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(description="""Gets all lesson types""")
async def aclesson_type_page(
        self, info: strawberry.types.Info
    ) -> List["AcLessonTypeGQLModel"]:
        loader = getLoaders(info).lessontypes
        rows = await loader.execute_select(loader.getSelectStatement())
        return rows
    
#################################################
# Mutation
#################################################
    
@strawberry.input
class LessonInsertGQLModel:
    topic_id:uuid.UUID
    type_id: uuid.UUID = strawberry.field(description="type of the lesson")
    count: Optional[int] = strawberry.field(description="count of the lessons", default=2)
    id: Optional[uuid.UUID] = None

@strawberry.input
class LessonUpdateGQLModel:
    id:uuid.UUID
    lastchange: datetime.datetime
    type_id: Optional[uuid.UUID] = None
    count: Optional[int] = None

@strawberry.type
class LessonResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of topic operation""")
    async def lesson(self, info: strawberry.types.Info) -> Union[AcLessonGQLModel, None]:
        result = await AcLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Adds new study lesson""")
async def lesson_insert(self, info: strawberry.types.Info, lesson: LessonInsertGQLModel) -> LessonResultGQLModel:
        loader = getLoaders(info).lessons
        row = await loader.insert(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(description="""Update the study lesson""")
async def lesson_update(self, info: strawberry.types.Info, lesson: LessonUpdateGQLModel) -> LessonResultGQLModel:
        loader = getLoaders(info).lessons
        row = await loader.update(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = lesson.id
        if row is None:
            result.msg = "fail"
            
        return result