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

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType


AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
PaymentGQLModel = typing.Annotated["PaymentGQLModel", strawberry.lazy(".PaymentGQLModel")]


@createInputs(v2=True)
class PaymentInfoInputFilter:
    id: IDType
    account_number: str
    specific_symbol: str
    constant_symbol: str
    IBAN: str
    SWIFT: str
    amount: float

@strawberry.federation.type(
    keys=["id"],
    description="one (in one year) admission linked to program"
)
class PaymentInfoGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        # loaders = getLoadersFromInfo(info)
        # print(f"loaders: {loaders}\n {dir(loaders)}")
        return getLoadersFromInfo(info).PaymentInfoModel   

    # admission_id: uuid.UUID = strawberry.field()
    account_number: typing.Optional[str] = strawberry.field(description="číslo účtu s kódem banky za lomítkem")
    specific_symbol: typing.Optional[str] = strawberry.field(description="specifický symbol")
    constant_symbol: typing.Optional[str] = strawberry.field(description="konstantní symbol")
    IBAN: typing.Optional[str] = strawberry.field(description="IBAN code")
    SWIFT: typing.Optional[str] = strawberry.field(description="SWIFT bank code")
    amount: typing.Optional[float] = strawberry.field(description="Částka k zaplacení")
    
    # admission: typing.Optional["AdmissionGQLModel"] = strawberry.field(
    #     description="",
    #     permission_classes=[
    #         OnlyForAuthentized
    #     ],
    #     resolver=ScalarResolver["AdmissionGQLModel"](fkey_field_name="admission_id")
    # )
    @strawberry.field(
        description="Přijímací řízení, kte kterému se tyto platební podmínky vztahují",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["AdmissionGQLModel"](fkey_field_name="admission_id")
    )    
    async def admission(self, info: strawberry.types.Info) -> typing.Optional["AdmissionGQLModel"]:
        from .AdmissionGQLModel import AdmissionGQLModel
        loader = AdmissionGQLModel.getLoader(info=info)
        rows = await loader.filter_by(payment_info_id=self.id)
        row = next(rows, None)
        result = AdmissionGQLModel.from_dataclass(row) if row else None
        return result
    
    payments: typing.List["PaymentGQLModel"] = strawberry.field(
        description="Všechny platby, které proběhly nebo byly uznány jako splnění těchto platebních podmínek",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["PaymentGQLModel"](fkey_field_name="payment_info_id", whereType=PaymentInfoInputFilter)
    )
    # async def payments(self, info: strawberry.types.Info) -> typing.List["PaymentGQLModel"]:
    #     from .PaymentGQLModel import PaymentGQLModel
    #     loader = PaymentGQLModel.getloader(info=info)
    #     rows = await loader.filter_by(payment_info_id=self.id)
    #     results = (PaymentGQLModel.from_sqlalchemy(row) for row in rows)
    #     return results
    #     # raise NotImplementedError()
    #     # from .AdmissionGQLModel import AdmissionGQLModel
    #     # result = await AdmissionGQLModel.resolve_reference(info=info, id=self.admission_id)
    #     # return result
        
    pass



@strawberry.interface(
    description=""
)
class PaymentInfoQuery:
    payment_info_by_id: typing.Optional["PaymentInfoGQLModel"] = strawberry.field(
        description="returns payment_info by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PaymentInfoGQLModel.load_with_loader
    )

    payment_info_page: typing.List["PaymentInfoGQLModel"] = strawberry.field(
        description="returns payment_infos defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["PaymentInfoGQLModel"](whereType=PaymentInfoInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class PaymentInfoInsertGQLModel(InputModelMixin):
    getLoader = PaymentInfoGQLModel.getLoader
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    account_number: typing.Optional[str] = strawberry.field(description="číslo účtu s kódem banky za lomítkem", default=None)
    specific_symbol: typing.Optional[str] = strawberry.field(description="specifický symbol", default=None)
    constant_symbol: typing.Optional[str] = strawberry.field(description="konstantní symbol", default=None)
    IBAN: typing.Optional[str] = strawberry.field(description="IBAN code", default=None)
    SWIFT: typing.Optional[str] = strawberry.field(description="SWIFT bank code", default=None)
    amount: typing.Optional[float] = strawberry.field(description="Částka k zaplacení", default=None)



@strawberry.input(
    description="parameter for update operation"
)
class PaymentInfoUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    account_number: typing.Optional[str] = strawberry.field(description="číslo účtu s kódem banky za lomítkem", default=strawberry.UNSET)
    specific_symbol: typing.Optional[str] = strawberry.field(description="specifický symbol", default=strawberry.UNSET)
    constant_symbol: typing.Optional[str] = strawberry.field(description="konstantní symbol", default=strawberry.UNSET)
    IBAN: typing.Optional[str] = strawberry.field(description="IBAN code", default=strawberry.UNSET)
    SWIFT: typing.Optional[str] = strawberry.field(description="SWIFT bank code", default=strawberry.UNSET)
    amount: typing.Optional[float] = strawberry.field(description="Částka k zaplacení", default=strawberry.UNSET)
    
@strawberry.input(
    description="parameter for delete operation"
)
class PaymentInfoDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class PaymentInfoMutation:

    @strawberry.mutation(
        description="create a new payment_info"
    )
    async def payment_info_insert(self, info: strawberry.types.Info, 
        payment_info: typing.Annotated[PaymentInfoInsertGQLModel, strawberry.argument(description="popis platebních podmínek pro vytvoření nových")]
    ) -> typing.Union[PaymentInfoGQLModel, InsertError[PaymentInfoGQLModel]]:
        result = await Insert[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)
        return result
    
    @strawberry.mutation(
        description="updates existing payment_info",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def payment_info_update(self, info: strawberry.types.Info, 
        payment_info: typing.Annotated[PaymentInfoUpdateGQLModel, strawberry.argument(description="popis platebních podmínek pro změnu existujících")]
    ) -> typing.Union[PaymentInfoGQLModel, UpdateError[PaymentInfoGQLModel]]:
        result = await Update[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)
        return result

    @strawberry.mutation(
        description="delete existing payment_info",
        permission_classes=[
            OnlyForAuthentized
        ]
    )
    async def payment_info_delete(self, info: strawberry.types.Info, 
        payment_info: typing.Annotated[PaymentInfoDeleteGQLModel, strawberry.argument(description="popis platebních podmínek, které mají být odstraněny")]
    ) -> typing.Optional[DeleteError[PaymentInfoGQLModel]]:
        result = await Delete[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)
        return result

