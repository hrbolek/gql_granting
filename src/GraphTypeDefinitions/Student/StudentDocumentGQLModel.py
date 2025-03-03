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

@createInputs
@dataclasses.dataclass
class StudentDocumentInputFilter:
    id: IDType

@strawberry.federation.type(
    description="documents related to the student",
    keys=["id"]
)
class StudentDocumentGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info) -> IDLoader:
        return getLoadersFromInfo(info=info).ProgramStudentDocumentModel
    
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



@strawberry.interface(
    description=""
)
class StudentDocumentQuery:
    student_document_by_id: typing.Optional["StudentDocumentGQLModel"] = strawberry.field(
        description="returns student_document by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=StudentDocumentGQLModel.load_with_loader
    )

    student_document_page: typing.List["StudentDocumentGQLModel"] = strawberry.field(
        description="returns student_documents defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["StudentDocumentGQLModel"](whereType=StudentDocumentInputFilter)
    )

@strawberry.input(
    description="parameter for create operation"
)
class StudentDocumentInsertGQLModel:
    name: str = strawberry.field(
        description="name of the student_document"
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)


@strawberry.input(
    description="parameter for update operation"
)
class StudentDocumentUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")

@strawberry.input(
    description="parameter for delete operation"
)
class StudentDocumentDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class StudentDocumentMutation:

    @strawberry.mutation(
        description="create a new student_document"
    )
    async def student_document_insert(self, info: strawberry.types.Info, student_document: StudentDocumentInsertGQLModel) -> typing.Union[StudentDocumentGQLModel, InsertError[StudentDocumentGQLModel]]:
        result = await Insert[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result
    
    @strawberry.mutation(
        description="updates existing student_document",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def student_document_update(self, info: strawberry.types.Info, student_document: StudentDocumentUpdateGQLModel) -> typing.Union[StudentDocumentGQLModel, UpdateError[StudentDocumentGQLModel]]:
        result = await Update[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result

    @strawberry.mutation(
        description="delete existing student_document",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def student_document_delete(self, info: strawberry.types.Info, student_document: StudentDocumentDeleteGQLModel) -> typing.Optional[DeleteError[StudentDocumentGQLModel]]:
        result = await Delete[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result

