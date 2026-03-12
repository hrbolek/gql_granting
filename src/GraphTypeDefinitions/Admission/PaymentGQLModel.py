import dataclasses
import strawberry
import uuid
import datetime
import typing

import strawberry.file_uploads
import strawberry.types

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
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from ..BaseGQLModel import BaseGQLModel, IDType, Relation

ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy(".ProgramGQLModel")]
AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
PaymentInfoGQLModel = typing.Annotated["PaymentInfoGQLModel", strawberry.lazy(".PaymentInfoGQLModel")]
StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy(".StudentGQLModel")]


@createInputs(v2=True)
class PaymentInputFilter:
    id: IDType
    user_id: IDType = strawberry.field(
        description="item for filtering by user id",
        directives=[Relation(to="UserGQLModel")]
    )
    program_id: IDType = strawberry.field(
        description="item for filtering by program id",
        directives=[Relation(to="ProgramGQLModel")]
    )
    bank_unique_data: str
    variable_symbol: str
    amount: float
    payment_info_id: IDType = strawberry.field(
        description="item for filtering by payment info id",
        directives=[Relation(to="PaymentInfoGQLModel")]
    )
    student_id: IDType = strawberry.field(
        description="item for filtering by student id",
        directives=[Relation(to="StudentGQLModel")]
    )
    lastchange: datetime.datetime
    created: datetime.datetime

@strawberry.federation.type(
    keys=["id"],
    description="one (in one year) admission linked to program"
    )
class PaymentGQLModel(BaseGQLModel):
   
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PaymentModel
    
    bank_unique_data: typing.Optional[str] = strawberry.field(description="unikátní identifikátor platby vystavený bankou (link do banky)")
    variable_symbol: typing.Optional[str] = strawberry.field(description="uvedený variabilní symbol")
    amount: typing.Optional[float] = strawberry.field(description="zaplacená částka")
    
    payment_info_id: typing.Optional[uuid.UUID] = strawberry.field(
        description="Generální platební podmínky",
        directives=[Relation(to="PaymentInfoGQLModel")]
    )
    student_id: typing.Optional[uuid.UUID] = strawberry.field(
        description="identifikovaná přihláška / student",
        directives=[Relation(to="StudentGQLModel")]
    )

    payment_info: typing.Optional["PaymentInfoGQLModel"] = strawberry.field(
        description="Informace o platebních podmínkách",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[PaymentInfoGQLModel](fkey_field_name="payment_info_id")
    )

    # from .StudentGQLModel import StudentGQLModel
    student: typing.Optional["StudentGQLModel"] = strawberry.field(
        description="Student, který měl platbu provést nebo platbu provedl",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StudentGQLModel](fkey_field_name="student_id")
    )

@strawberry.interface(
    description=""
)
class PaymentQuery:
    payment_by_id: typing.Optional["PaymentGQLModel"] = strawberry.field(
        description="returns payment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PaymentGQLModel.load_with_loader
    )

    payment_page: typing.List["PaymentGQLModel"] = strawberry.field(
        description="returns payments defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["PaymentGQLModel"](whereType=PaymentInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class PaymentInsertGQLModel(InputModelMixin):
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    student_id: typing.Optional[IDType] = strawberry.field(
        description="student id", 
        default=None, 
        directives=[
            Relation(to="StudentGQLModel")
        ]
    )
    program_id: typing.Optional[IDType] = strawberry.field(
        description="program id", 
        default=None,
        directives=[
            Relation(to="ProgramGQLModel")
        ]
    )
    bank_unique_data: typing.Optional[str] = strawberry.field(description="unikátní identifikátor platby vystavený bankou (link do banky)", default=None)
    variable_symbol: typing.Optional[str] = strawberry.field(description="uvedený variabilní symbol", default=None)
    amount: typing.Optional[float] = strawberry.field(description="zaplacená částka", default=None)
    payment_info_id: typing.Optional[IDType] = strawberry.field(
        description="Generální platební podmínky", 
        default=None,
        directives=[
            Relation(to="PaymentInfoGQLModel")
        ]
    )


@strawberry.input(
    description="parameter for update operation"
)
class PaymentUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    student_id: typing.Optional[IDType] = strawberry.field(
        description="student id", 
        default=None,
        directives=[
            Relation(to="StudentGQLModel")
        ]
    )
    program_id: typing.Optional[IDType] = strawberry.field(
        description="program id", 
        default=None,
        directives=[
            Relation(to="ProgramGQLModel")
        ]
    )
    bank_unique_data: typing.Optional[str] = strawberry.field(description="unikátní identifikátor platby vystavený bankou (link do banky)", default=None)
    variable_symbol: typing.Optional[str] = strawberry.field(description="uvedený variabilní symbol", default=None)
    amount: typing.Optional[float] = strawberry.field(description="zaplacená částka", default=None)
    payment_info_id: typing.Optional[IDType] = strawberry.field(
        description="Generální platební podmínky", 
        default=None,
        directives=[
            Relation(to="PaymentInfoGQLModel")
        ]
    )

@strawberry.input(
    description="parameter for delete operation"
)
class PaymentDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class PaymentMutation:

    @strawberry.mutation(
        description="create a new payment"
    )
    async def payment_insert(self, info: strawberry.types.Info, 
        payment: typing.Annotated[PaymentInsertGQLModel, strawberry.argument(description="definice pro uložení nové platby")]
    ) -> typing.Union[PaymentGQLModel, InsertError[PaymentGQLModel]]:
        result = await Insert[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)
        return result
    
    @strawberry.mutation(
        description="updates existing payment",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def payment_update(self, info: strawberry.types.Info, 
        payment: typing.Annotated[PaymentUpdateGQLModel, strawberry.argument(description="definice pro změnu platby")]
    ) -> typing.Union[PaymentGQLModel, UpdateError[PaymentGQLModel]]:
        result = await Update[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)
        return result

    @strawberry.mutation(
        description="delete existing payment",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def payment_delete(self, info: strawberry.types.Info, 
        payment: typing.Annotated[PaymentDeleteGQLModel, strawberry.argument(description="definice pro odstranění platby")]
    ) -> typing.Optional[DeleteError[PaymentGQLModel]]:
        result = await Delete[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)
        return result

