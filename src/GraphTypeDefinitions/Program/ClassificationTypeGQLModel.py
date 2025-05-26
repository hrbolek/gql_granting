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


@strawberry.federation.type(
    description=""
)
class ClassificationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ClassificationTypeModel
    
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="the name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="the name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )    
    