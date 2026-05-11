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
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from uoishelpers.dataloaders import IDLoader
from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType


StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy(".StudentGQLModel")]
DocumentGQLModel = typing.Annotated["DocumentGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_Office.DocumentGQLModel")]

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
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )        

    student_id: typing.Optional[IDType] = strawberry.field(
        description="id of the study / no user_id",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    student: typing.Optional["StudentGQLModel"] = strawberry.field(
        description="student",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StudentGQLModel"](fkey_field_name="student_id")
    )

    document_id: typing.Optional[IDType] = strawberry.field(
        description="id of the document",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )        

    document: typing.Optional["DocumentGQLModel"] = strawberry.field(
        description="document",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["DocumentGQLModel"](fkey_field_name="document_id")
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
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    # description: typing.Optional[str] = strawberry.field(description="description", default=None)
    student_id: IDType = strawberry.field(description="id of the study / no user_id")
    document_id: IDType = strawberry.field(description="id of the document")

    rbacobject_id: strawberry.Private[IDType] = None
    created_by: strawberry.Private[IDType] = None

@strawberry.input(
    description="parameter for update operation"
)
class StudentDocumentUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    # description: typing.Optional[str] = strawberry.field(description="description", default=strawberry.UNSET)
    student_id: typing.Optional[IDType] = strawberry.field(description="id of the study / no user_id", default=strawberry.UNSET)
    document_id: typing.Optional[IDType] = strawberry.field(description="id of the document", default=strawberry.UNSET)
    
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
    from .StudentGQLModel import StudentGQLModel
    @strawberry.mutation(
        description="create a new student_document",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, StudentDocumentGQLModel](roles=["studijní administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, StudentDocumentGQLModel](),
            RbacProviderExtension[InsertError, StudentDocumentGQLModel](),
            LoadDataExtension[InsertError, StudentDocumentGQLModel](
                primary_key_name="student_id",
                getLoader=StudentGQLModel.getLoader
            )
        ]
    )
    async def student_document_insert(
        self, 
        info: strawberry.types.Info, 
        student_document: StudentDocumentInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudentDocumentGQLModel, InsertError[StudentDocumentGQLModel]]:
        student_document.rbacobject_id = rbacobject_id
        result = await Insert[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result
    
    @strawberry.mutation(
        description="updates existing student_document",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, StudentDocumentGQLModel](
                roles=["studijní administrátor", "personalista"]),
            UserRoleProviderExtension[UpdateError, StudentDocumentGQLModel](),
            RbacProviderExtension[UpdateError, StudentDocumentGQLModel](),
            LoadDataExtension[UpdateError, StudentDocumentGQLModel]()
        ]
    )
    async def student_document_update(
        self, 
        info: strawberry.types.Info, 
        student_document: StudentDocumentUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[StudentDocumentGQLModel, UpdateError[StudentDocumentGQLModel]]:
        result = await Update[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result

    @strawberry.mutation(
        description="delete existing student_document",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, StudentDocumentGQLModel](roles=["studijní administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, StudentDocumentGQLModel](),
            RbacProviderExtension[DeleteError, StudentDocumentGQLModel](),
            LoadDataExtension[DeleteError, StudentDocumentGQLModel]()
        ]
    )
    async def student_document_delete(
        self, 
        info: strawberry.types.Info, 
        student_document: StudentDocumentDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[StudentDocumentGQLModel]]:
        result = await Delete[StudentDocumentGQLModel].DoItSafeWay(info=info, entity=student_document)
        return result

