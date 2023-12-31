from doctest import master
from functools import cache
from gql_granting.DBDefinitions import BaseModel

import random
import itertools
from functools import cache


from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result

import datetime

from gql_granting.DBDefinitions import (
    
    ProgramFormTypeModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramModel,
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel,
    
    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,


)

import asyncio
import os
import json

from uoishelpers.feeders import ImportModels

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "_________"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,
            ClassificationLevelModel,
            ClassificationTypeModel,

            ProgramModel,
            SubjectModel,
            SemesterModel,
            TopicModel,
            LessonModel,
            ClassificationModel,
        ]
    else:
        dbModels = [
            ProgramFormTypeModel,
            ProgramLanguageTypeModel,
            ProgramLevelTypeModel,
            ProgramTitleTypeModel,
            ProgramTypeModel,
            LessonTypeModel,
            ClassificationLevelModel,
            ClassificationTypeModel,

            ProgramModel,
            SubjectModel,
            SemesterModel,
            TopicModel,
            LessonModel,
            ClassificationModel,

        ]
        
    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass
