import strawberry
import typing
import datetime
import uuid
import logging

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel


from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    createRootResolver_by_id,
)
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

#UserGQLModel= Annotated["UserGQLModel",strawberry.lazy(".granting")]

@strawberry.federation.type(
    keys=["id"], 
    description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).classificationtypes
        return loader

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    lastchange = resolve_lastchange
    
#################################################
# Query
#################################################

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs 

@createInputs
@dataclass 
class ClassificationTypeWhereFilter: 
    name : str 
    name_en : str 

from ._GraphResolvers import asPage

@strawberry.field(
    description="""Finds a classification type by its id""",
    permission_classes=[OnlyForAuthentized()])
async def acclassification_type_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[AcClassificationTypeGQLModel]:
        result = await AcClassificationTypeGQLModel.resolve_reference(info=info, id=id)
        return result

@strawberry.field(
    description="""Lists classifications types""",
    permission_classes=[OnlyForAuthentized()])
@asPage
async def acclassification_type_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
        where: typing.Optional[ClassificationTypeWhereFilter] = None
    ) -> typing.List[AcClassificationTypeGQLModel]:
        # wf = None if where is None else strawberry.asdict(where)
        # loader = getLoadersFromInfo(info).classificationtypes
        # result = await loader.page(skip, limit, where=wf)
        # return result    
        return getLoadersFromInfo(info).classificationtypes

