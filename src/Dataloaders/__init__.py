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


# @cache
# def composeAuthUrl():
#     hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
#     assert hostname is not None, "undefined GQLUG_ENDPOINT_URL"
#     assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
#     assert "." not in hostname, "security check failed, change source code"
#     return hostname

# class AuthorizationLoader(DataLoader):

#     query = """query($id: UUID!){result: rbacById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
#             # variables = {"id": rbacobject}

#     roleUrlEndpoint=None#composeAuthUrl()
#     def __init__(self,
#         roleUrlEndpoint=roleUrlEndpoint,
#         query=query,
#         demo=True):
#         super().__init__(cache=True)
#         self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
#         self.query = query
#         self.demo = demo
#         self.authorizationToken = ""

#     def setTokenByInfo(self, info):
#         self.authorizationToken = ""

#     async def _load(self, id):
#         variables = {"id": f"{id}"}
#         if self.authorizationToken != "":
#             headers = {"authorization": f"Bearer {self.authorizationToken}"}
#         else:
#             headers = {}
#         json = {
#             "query": self.query,
#             "variables": variables
#         }
#         roleUrlEndpoint=self.roleUrlEndpoint
#         async with aiohttp.ClientSession() as session:
#             print(f"query {roleUrlEndpoint} for json={json}")
#             async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
#                 print(resp.status)
#                 if resp.status != 200:
#                     text = await resp.text()
#                     print(text)
#                     return []
#                 else:
#                     respJson = await resp.json()

#         # print(20*"respJson")
#         # print(respJson)
        
#         assert respJson.get("errors", None) is None, respJson["errors"]
#         respdata = respJson.get("data", None)
#         assert respdata is not None, "missing data response"
#         result = respdata.get("result", None)
#         assert result is not None, "missing result"
#         roles = result.get("roles", None)
#         assert roles is not None, "missing roles"
        
#         # print(30*"=")
#         # print(roles)
#         # print(30*"=")
#         return [*roles]


#     async def batch_load_fn(self, keys):
#         #print('batch_load_fn', keys, flush=True)
#         reducedkeys = set(keys)
#         awaitables = (self._load(key) for key in reducedkeys)
#         results = await asyncio.gather(*awaitables)
#         indexedResult = {key:result for key, result in zip(reducedkeys, results)}
#         results = [indexedResult[key] for key in keys]
#         return results
    


# async def createLoaders_3(asyncSessionMaker):

#     class Loaders:
#         @property
#         @cache
#         def acprogramform_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramFormTypeModel)

#         @property
#         @cache
#         def acprogramlanguage_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramLanguageTypeModel)

#         @property
#         @cache
#         def acprogramlevel_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramLevelTypeModel)

#         @property
#         @cache
#         def acprogramtitle_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramTitleTypeModel)

#         @property
#         @cache
#         def acprogramtype_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramTypeModel)

#         @property
#         @cache
#         def acclassificationlevel_by_id(self):
#             return createIdLoader(asyncSessionMaker, ClassificationLevelModel)

#         @property
#         @cache
#         def acclassificationtype_by_id(self):
#             return createIdLoader(asyncSessionMaker, ClassificationTypeModel)

#         @property
#         @cache
#         def aclessontype_by_id(self):
#             return createIdLoader(asyncSessionMaker, LessonTypeModel)

#         @property
#         @cache
#         def acprogramgroup_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramGroupModel)

#         @property
#         @cache
#         def acprogram_by_id(self):
#             return createIdLoader(asyncSessionMaker, ProgramModel)

#         @property
#         @cache
#         def acsubject_by_id(self):
#             return createIdLoader(asyncSessionMaker, SubjectModel)

#         @property
#         @cache
#         def acsubject_for_program(self):
#             return createFkeyLoader(asyncSessionMaker, SubjectModel, foreignKeyName="program_id")

#         @property
#         @cache
#         def acsemester_for_subject(self):
#             return createFkeyLoader(asyncSessionMaker, SemesterModel, foreignKeyName="subject_id")

#         @property
#         @cache
#         def acsemester_by_id(self):
#             return createIdLoader(asyncSessionMaker, SemesterModel)

#         @property
#         @cache
#         def actopic_by_id(self):
#             return createIdLoader(asyncSessionMaker, TopicModel)

#         @property
#         @cache
#         def actopics_for_semester(self):
#             return createFkeyLoader(asyncSessionMaker, TopicModel, foreignKeyName="semester_id")

#         @property
#         @cache
#         def aclesson_by_id(self):
#             return createIdLoader(asyncSessionMaker, LessonModel)

#         @property
#         @cache
#         def aclessons_for_topic(self):
#             return createFkeyLoader(asyncSessionMaker, LessonModel, foreignKeyName="topic_id")

#         @property
#         @cache
#         def acclassification_by_id(self):
#             return createIdLoader(asyncSessionMaker, ClassificationModel)

#         @property
#         @cache
#         def acclassification_for_semester(self):
#             return createFkeyLoader(asyncSessionMaker, ClassificationModel, foreignKeyName="semester_id")

#     return Loaders()

# dbmodels = {
#     "programforms": ProgramFormTypeModel,
#     "programlanguages": ProgramLanguageTypeModel,
#     "programleveltypes": ProgramLevelTypeModel,
#     "programs": ProgramModel,
#     "programtitletypes": ProgramTitleTypeModel,
#     "programtypes": ProgramTypeModel,
#     "programstudents": ProgramStudentModel,
#     "programmessages": ProgramStudentMessageModel,
#     # "acprograms_studentstates": ProgramStudentStateModel,

#     "classificationlevels": ClassificationLevelModel,
#     "classifications": ClassificationModel,
#     "classificationtypes": ClassificationTypeModel,
    
#     "subjects": SubjectModel,
#     "semesters": SemesterModel,
#     "topics": TopicModel,
#     "lessons": LessonModel,
#     "lessontypes": LessonTypeModel
# }

# def createLoaders(asyncSessionMaker, models=dbmodels):
#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
#     attrs = {}
#     for key, DBModel in models.items():
#         attrs[key] = property(cache(createLambda(key, DBModel)))
#         cls = DBModel
#         attrs[cls.__tablename__] = property(cache(createLambda(None, cls)))
#         attrs[cls.__name__] = attrs[cls.__tablename__]
#         print("loader", cls.__tablename__, cls.__name__)

#     attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

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
