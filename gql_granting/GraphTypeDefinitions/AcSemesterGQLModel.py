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

#from .AcTopicGQLModel import AcTopicGQLModel
from .AcClassificationTypeGQLModel import AcClassificationTypeGQLModel
#from .AcClassificationGQLModel import AcClassificationGQLModel

AcClassificationGQLModel= Annotated["AcClassificationGQLModel",strawberry.lazy(".AcClassificationGQLModel")]
AcTopicGQLModel= Annotated["AcTopicGQLModel",strawberry.lazy(".AcTopicGQLModel")]
AcSubjectGQLModel=Annotated["AcSubjectGQLModel",strawberry.lazy(".AcSubjectGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing each semester in study subject"""
)
class AcSemesterGQLModel:
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).semesters
        return loader

    @strawberry.field(description="""primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""semester number""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="""credits""")
    def credits(self) -> int:
        return self.credits

    @strawberry.field(description="""credits""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


    # FK###############################################################################################
    @strawberry.field(description="""Subject related to the semester (semester owner)""")
    async def subject(self, info: strawberry.types.Info) -> Optional["AcSubjectGQLModel"]:
        from .AcSubjectGQLModel import AcSubjectGQLModel
        result = await AcSubjectGQLModel.resolve_reference(info, self.subject_id)
        return result

    @strawberry.field(description="""Subject related to the semester (semester owner)""")
    async def classification_type(self, info: strawberry.types.Info) -> "AcClassificationTypeGQLModel":
        result = await AcClassificationTypeGQLModel.resolve_reference(info, self.classificationtype_id)
        return result

    @strawberry.field(description="""Final classification of the semester""")
    async def classifications(
        self, info: strawberry.types.Info
    ) -> List["AcClassificationGQLModel"]:
        #loader = getLoaders(info).acclassification_for_semester
        loader = getLoaders(info).classifications
        result = await loader.filter_by(semester_id=self.id)
        return result

    @strawberry.field(description="""topics""")
    async def topics(self, info: strawberry.types.Info) -> List["AcTopicGQLModel"]:
        loader = getLoaders(info).topics
        result = await loader.filter_by(semester_id=self.id)
        return result

#################################################
#
# Special fields for query
#
#################################################

@strawberry.field(description="""Finds a subject semester by its id""")
async def acsemester_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union["AcSemesterGQLModel", None]:
        result = await AcSemesterGQLModel.resolve_reference(info, id)
        return result

@strawberry.field(description="""Finds a subject semester by its id""")
async def acsemester_page(
        self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.page(skip=skip, limit=limit)
        return result


    
#################################################
#
# Special fields for query
#
#################################################

@strawberry.field(description="""Finds a subject semester by its id""")
async def acsemester_page(
        self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.page(skip=skip, limit=limit)
        return result

#################################################
#
# Special fields for mutation
#
#################################################

@strawberry.input
class SemesterInsertGQLModel:
    subject_id:uuid.UUID
    classificationtype_id: uuid.UUID
    order: Optional[int] = 0
    credits: Optional[int] = 0
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True

@strawberry.input
class SemesterUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    order: Optional[int] = None
    credits: Optional[int] = None
    classificationtype_id: Optional[uuid.UUID] = None

@strawberry.type
class SemesterResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of semester operation""")
    async def semester(self, info: strawberry.types.Info) -> Union[AcSemesterGQLModel, None]:
        result = await AcSemesterGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Adds a new semester to study program""")
async def semester_insert(self, info: strawberry.types.Info, semester: SemesterInsertGQLModel) -> SemesterResultGQLModel:
        loader = getLoaders(info).semesters
        row = await loader.insert(semester)
        print("semester_insert", row.id, row.classificationtype_id)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberry.mutation(description="""Update the semester of study program""")
async def semester_update(self, info: strawberry.types.Info, semester: SemesterUpdateGQLModel) -> SemesterResultGQLModel:
        loader = getLoaders(info).semesters
        row = await loader.update(semester)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = semester.id
        if row is None:
            result.msg = "fail"
            
        return result