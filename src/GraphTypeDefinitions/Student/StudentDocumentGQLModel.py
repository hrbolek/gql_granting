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

from uoishelpers.dataloaders import IDLoader
from ..BaseGQLModel import BaseGQLModel, IDType

StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy(".StudentGQLModel")]
DocumentGQLModel = typing.Annotated["DocumentGQLModel", strawberry.lazy("..DocumentGQLModel")]

@strawberry.federation.type(
    description="documents related to the student",
    keys=["id"]
)
class StudentDocumentGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info) -> IDLoader:
        return getLoadersFromInfo(info=info).StudentDocumentModel
    
    description: typing.Optional[str] = strawberry.field(
        description="description",
        permission_classes=[
            OnlyForAuthentized
        ]
    )        

    student_id: typing.Optional[IDType] = strawberry.field(
        description="id of the student",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    student: typing.Optional["StudentGQLModel"] = strawberry.field(
        description="student",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    document_id: typing.Optional[IDType] = strawberry.field(
        description="id of the document",
        permission_classes=[
            OnlyForAuthentized
        ]
    )        

    document: typing.Optional["DocumentGQLModel"] = strawberry.field(
        description="document",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
