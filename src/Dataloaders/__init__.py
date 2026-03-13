import os
import asyncio
import aiohttp
from functools import cache

from aiodataloader import DataLoader

from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from uoishelpers.dataloaders import createLoadersAuto


from ..DBDefinitions import (
    BaseModel, 
    ProgramFormTypeModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramStudentModel,
    ProgramStudentDocumentModel,
    ProgramStudentMessageModel,

    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,
    
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel,

    PlanModel,
    PlanItemFacilityModel,
    PlanItemGroupModel,
    PlanItemTeacherModel,
    PlanItemModel,

    ClassificationPlanModel,

    AdmissionModel,
    PaymentInfoModel,
    PaymentModel
)


def createLoadersContext(asyncSessionMaker):
    return {
        # "loaders": createLoaders(asyncSessionMaker)
        "loaders": createLoadersAuto(asyncSessionMaker, BaseModel=BaseModel)
    }

from uoishelpers.dataloaders import createIdLoader
from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
from functools import cache
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel
    ProgramFormTypeModel: IDLoader[src.DBDefinitions.ProgramFormTypeModel] = None
    ProgramLanguageTypeModel: IDLoader[src.DBDefinitions.ProgramLanguageTypeModel] = None
    ProgramLevelTypeModel: IDLoader[src.DBDefinitions.ProgramLevelTypeModel] = None
    ProgramModel: IDLoader[src.DBDefinitions.ProgramModel] = None
    ProgramTitleTypeModel: IDLoader[src.DBDefinitions.ProgramTitleTypeModel] = None
    ProgramTypeModel: IDLoader[src.DBDefinitions.ProgramTypeModel] = None
    ProgramStudentModel: IDLoader[src.DBDefinitions.ProgramStudentModel] = None
    ProgramStudentDocumentModel: IDLoader[src.DBDefinitions.ProgramStudentDocumentModel] = None
    ProgramStudentMessageModel: IDLoader[src.DBDefinitions.ProgramStudentMessageModel] = None

    ClassificationLevelModel: IDLoader[src.DBDefinitions.ClassificationLevelModel] = None
    ClassificationModel: IDLoader[src.DBDefinitions.ClassificationModel] = None
    ClassificationTypeModel: IDLoader[src.DBDefinitions.ClassificationTypeModel] = None
    
    SubjectModel: IDLoader[src.DBDefinitions.SubjectModel] = None
    SemesterModel: IDLoader[src.DBDefinitions.SemesterModel] = None
    TopicModel: IDLoader[src.DBDefinitions.TopicModel] = None
    LessonModel: IDLoader[src.DBDefinitions.LessonModel] = None
    LessonTypeModel: IDLoader[src.DBDefinitions.LessonTypeModel] = None

    PlanModel: IDLoader[src.DBDefinitions.PlanModel] = None
    PlanItemFacilityModel: IDLoader[src.DBDefinitions.PlanItemFacilityModel] = None
    PlanItemGroupModel: IDLoader[src.DBDefinitions.PlanItemGroupModel] = None
    PlanItemTeacherModel: IDLoader[src.DBDefinitions.PlanItemTeacherModel] = None
    PlanItemModel: IDLoader[src.DBDefinitions.PlanItemModel] = None

    ClassificationPlanModel: IDLoader[src.DBDefinitions.ClassificationPlanModel] = None

    AdmissionModel: IDLoader[src.DBDefinitions.AdmissionModel] = None
    PaymentInfoModel: IDLoader[src.DBDefinitions.PaymentInfoModel] = None
    PaymentModel: IDLoader[src.DBDefinitions.PaymentModel] = None

    def __init__(self, session):
        super().__init__(session)

        self.ProgramFormTypeModel = self.get(ProgramFormTypeModel)
        self.ProgramLanguageTypeModel = self.get(ProgramLanguageTypeModel)
        self.ProgramLevelTypeModel = self.get(ProgramLevelTypeModel)
        self.ProgramModel = self.get(ProgramModel)
        self.ProgramTitleTypeModel = self.get(ProgramTitleTypeModel)
        self.ProgramTypeModel = self.get(ProgramTypeModel)
        self.ProgramStudentModel = self.get(ProgramStudentModel)
        self.ProgramStudentDocumentModel = self.get(ProgramStudentDocumentModel)
        self.ProgramStudentMessageModel = self.get(ProgramStudentMessageModel)

        self.ClassificationLevelModel = self.get(ClassificationLevelModel)
        self.ClassificationModel = self.get(ClassificationModel)
        self.ClassificationTypeModel = self.get(ClassificationTypeModel)
        
        self.SubjectModel = self.get(SubjectModel)
        self.SemesterModel = self.get(SemesterModel)
        self.TopicModel = self.get(TopicModel)
        self.LessonModel = self.get(LessonModel)
        self.LessonTypeModel = self.get(LessonTypeModel)

        self.PlanModel = self.get(PlanModel)
        self.PlanItemFacilityModel = self.get(PlanItemFacilityModel)
        self.PlanItemGroupModel = self.get(PlanItemGroupModel)
        self.PlanItemTeacherModel = self.get(PlanItemTeacherModel)
        self.PlanItemModel = self.get(PlanItemModel)

        self.ClassificationPlanModel = self.get(ClassificationPlanModel)

        self.AdmissionModel = self.get(AdmissionModel)
        self.PaymentInfoModel = self.get(PaymentInfoModel)
        self.PaymentModel = self.get(PaymentModel)

        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
