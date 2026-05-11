import strawberry
import uuid
import datetime
import typing
import dataclasses

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

from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType, Relation

ProgramGQLModel = typing.Annotated["ProgramGQLModel", strawberry.lazy("..Program.ProgramGQLModel")]
PaymentInfoGQLModel = typing.Annotated["PaymentInfoGQLModel", strawberry.lazy(".PaymentInfoGQLModel")]
PaymentInfoInputFilter = typing.Annotated["PaymentInfoInputFilter", strawberry.lazy(".PaymentInfoGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy("src.GraphTypeDefinitions.Domain_UG.StateGQLModel")]

@createInputs(v2=True)
# @dataclasses.dataclass
class AdmissionInputFilter:
    id: IDType
    program_id: IDType = strawberry.field(
        description="Filter for program id", 
        directives=[Relation(to="ProgramGQLModel")]
    )
    state_id: IDType = strawberry.field(
        description="Filter for state id", 
        directives=[Relation(to="StateGQLModel")]
    )
    payment_info_id: IDType = strawberry.field(
        description="Filter for paymentInfo id", 
        directives=[Relation(to="PaymentInfoGQLModel")]
    )

    name: str
    name_en: str
    application_start_date: datetime.datetime
    application_last_date: datetime.datetime    
    end_date: datetime.datetime
    condition_date: datetime.datetime
    payment_date: datetime.datetime
    condition_extended_date: datetime.datetime
    request_condition_extend_date: datetime.datetime
    request_extra_conditions_date: datetime.datetime
    request_extra_date_date: datetime.datetime
    exam_start_date: datetime.datetime
    exam_last_date: datetime.datetime
    student_entry_date: datetime.datetime

    payment_info: PaymentInfoInputFilter



@strawberry.federation.type(
    keys=["id"],
    description="one (in one year) admission linked to program"
)
class AdmissionGQLModel(BaseGQLModel):
   
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).AdmissionModel

    name: typing.Optional[str] = strawberry.field(description="name", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name en", default=None)

    state_id: typing.Optional[IDType] = strawberry.field(
        description="stav přijímacího řízení", 
        default=None,
        directives=[Relation(to="StateGQLModel")]
    )
    program_id: typing.Optional[IDType] = strawberry.field(
        description="Program, pro který je přijímací řízení vypsáno", 
        default=None,
        directives=[Relation(to="ProgramGQLModel")]
    )
    payment_info_id: typing.Optional[IDType] = strawberry.field(
        description="platební podmínky", 
        default=None,
        directives=[Relation(to="PaymentInfoGQLModel")]
    )

    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy lze podávat přihlášky", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možnost podání přihlášky", default=None)
    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Konec přijímacího řízení", default=None)
    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze doložit splnění podmínek", default=None)
    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=None)
    condition_extended_date: typing.Optional[datetime.datetime] = strawberry.field(description="Prodloužená lhůta pro doložení splnění podmínek", default=None)
    request_condition_extend_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o proudloužení pro doložení splnění podmínek", default=None)
    request_extra_conditions_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o specifické podmínky přijímacího řízení", default=None)
    request_extra_date_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o extra termín přijímacích zkoušek", default=None)
    exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="První možný den přijímacích zkoušek", default=None)
    exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možný den přijímacích zkoušek", default=None)
    student_entry_date: typing.Optional[datetime.datetime] = strawberry.field(description="Den zápisu", default=None)

    program: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="Program, ke kterému je přijímací řízení",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProgramGQLModel"](fkey_field_name="program_id")
    )
    # async def program(self, info: strawberry.types.Info) -> typing.Optional["ProgramGQLModel"]:
    #     from .ProgramGQLModel import ProgramGQLModel
    #     result = await ProgramGQLModel.resolve_reference(info=info, id=self.program_id)
    #     return result

    payment_info: typing.Optional["PaymentInfoGQLModel"] = strawberry.field(
        description="Pokyny k platbě",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["PaymentInfoGQLModel"](fkey_field_name="payment_info_id")
    )

    # async def payment_info(self, info: strawberry.types.Info) -> typing.Optional["PaymentInfoGQLModel"]:
    #     from .PaymentInfoGQLModel import PaymentInfoGQLModel
    #     result = await PaymentInfoGQLModel.load_with_loader(info=info, id=self.payment_info_id)
    #     return result

    state: typing.Optional["StateGQLModel"] = strawberry.field(
        description="Stav přijímacího řízení",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["StateGQLModel"](fkey_field_name="state_id")
    )
    # async def state(self, info: strawberry.types.Info) -> typing.Optional["StateGQLModel"]:
    #     from .StateGQLModel import StateGQLModel
    #     result = await StateGQLModel.resolve_reference(info=info, id=self.state_id)
    #     return result

@strawberry.interface(description="")
class AdmissionQuery:
    admission_by_id: typing.Optional[AdmissionGQLModel] = strawberry.field(
        description="Přijímací řízení pro specifické ID",
        resolver=AdmissionGQLModel.load_with_loader
    )

    admission_page: typing.List[AdmissionGQLModel] = strawberry.field(
        description="Seznam přijímacích řízení",
        resolver=PageResolver[AdmissionGQLModel](whereType=AdmissionInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class AdmissionInsertGQLModel(InputModelMixin):
    getLoader = AdmissionGQLModel.getLoader
    program_id: IDType = strawberry.field(
        description="program the admission is linked with",
        directives=[Relation(to="ProgramGQLModel")]
    )
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    name: typing.Optional[str] = strawberry.field(description="name", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name en", default=None)
    state_id: typing.Optional[IDType] = strawberry.field(
        description="stav přijímacího řízení", 
        default=None,
        directives=[
            Relation(to="StateGQLModel")
        ]
    )
    payment_info_id: typing.Optional[IDType] = strawberry.field(
        description="platební podmínky", 
        default=None,
        directives=[
            Relation(to="PaymentInfoGQLModel")
        ]
    )
    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy lze podávat přihlášky", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možnost podání přihlášky", default=None)
    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Konec přijímacího řízení", default=None)
    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze doložit splnění podmínek", default=None)
    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=None)
    condition_extended_date: typing.Optional[datetime.datetime] = strawberry.field(description="Prodloužená lhůta pro doložení splnění podmínek", default=None)
    request_condition_extend_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o prodloužení pro doložení splnění podmínek", default=None)
    request_extra_conditions_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o specifické podmínky přijímacího řízení", default=None)
    request_extra_date_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o extra termín přijímacích zkoušek", default=None)
    exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="První možný den přijímacích zkoušek", default=None)
    exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možný den přijímacích zkoušek", default=None)
    student_entry_date: typing.Optional[datetime.datetime] = strawberry.field(description="Den zápisu", default=None)
    
    rbacobject_id: strawberry.Private[IDType] = None
    created_by: strawberry.Private[IDType] = None

@strawberry.input(
    description="parameter for update operation"
)
class AdmissionUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name", default=strawberry.UNSET)
    name_en: typing.Optional[str] = strawberry.field(description="name en", default=strawberry.UNSET)
    state_id: typing.Optional[IDType] = strawberry.field(
        description="stav přijímacího řízení", 
        default=strawberry.UNSET,
        directives=[
            Relation(to="StateGQLModel")
        ]
    )
    payment_info_id: typing.Optional[IDType] = strawberry.field(
        description="platební podmínky", 
        default=strawberry.UNSET,
        directives=[
            Relation(to="PaymentInfoGQLModel")
        ]
    )
    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy lze podávat přihlášky", default=strawberry.UNSET)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možnost podání přihlášky", default=strawberry.UNSET)
    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Konec přijímacího řízení", default=strawberry.UNSET)
    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze doložit splnění podmínek", default=strawberry.UNSET)
    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=strawberry.UNSET)
    condition_extended_date: typing.Optional[datetime.datetime] = strawberry.field(description="Prodloužená lhůta pro doložení splnění podmínek", default=strawberry.UNSET)
    request_condition_extend_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o prodloužení pro doložení splnění podmínek", default=strawberry.UNSET)
    request_extra_conditions_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o specifické podmínky přijímacího řízení", default=strawberry.UNSET)
    request_extra_date_date: typing.Optional[datetime.datetime] = strawberry.field(description="Lhůta do kdy lze požádat o extra termín přijímacích zkoušek", default=strawberry.UNSET)
    exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="První možný den přijímacích zkoušek", default=strawberry.UNSET)
    exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Poslední možný den přijímacích zkoušek", default=strawberry.UNSET)
    student_entry_date: typing.Optional[datetime.datetime] = strawberry.field(description="Den zápisu", default=strawberry.UNSET)
    
@strawberry.input(
    description="parameter for delete operation"
)
class AdmissionDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class AdmissionMutation:
    from ..Program.ProgramGQLModel import ProgramGQLModel
    @strawberry.mutation(
        description="create a new admission",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, AdmissionGQLModel](
                roles=["studijní administrátor"]),
            UserRoleProviderExtension[InsertError, AdmissionGQLModel](),
            RbacProviderExtension[InsertError, AdmissionGQLModel](),
            LoadDataExtension[InsertError, AdmissionGQLModel](
                primary_key_name="program_id",
                getLoader=ProgramGQLModel.getLoader
            )
        ]
    )
    async def admission_insert(
        self, 
        info: strawberry.types.Info, 
        admission: typing.Annotated[AdmissionInsertGQLModel, strawberry.argument(
            description="Vstupní data pro vytvoření přijímací řízení"
        )],
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[AdmissionGQLModel, InsertError[AdmissionGQLModel]]:
        admission.rbacobject_id = rbacobject_id
        result = await Insert[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
        return result
    
    @strawberry.mutation(
        description="updates existing admission",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, AdmissionGQLModel](
                roles=["studijní administrátor"]),
            UserRoleProviderExtension[InsertError, AdmissionGQLModel](),
            RbacProviderExtension[InsertError, AdmissionGQLModel](),
            LoadDataExtension[InsertError, AdmissionGQLModel]()
        ]
    )
    async def admission_update(self, info: strawberry.types.Info, 
        admission: typing.Annotated[AdmissionUpdateGQLModel, strawberry.argument(
            description="Vstupní data pro úpravu přijímací řízení"
        )],
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[AdmissionGQLModel, UpdateError[AdmissionGQLModel]]:
        result = await Update[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
        return result

    @strawberry.mutation(
        description="delete existing admission",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, AdmissionGQLModel](
                roles=["studijní administrátor"]),
            UserRoleProviderExtension[InsertError, AdmissionGQLModel](),
            RbacProviderExtension[InsertError, AdmissionGQLModel](),
            LoadDataExtension[InsertError, AdmissionGQLModel]()
        ]
    )
    async def admission_delete(
        self, 
        info: strawberry.types.Info, 
        admission: typing.Annotated[AdmissionDeleteGQLModel, strawberry.argument(
            description="Vstupní data pro smazání přijímací řízení"
        )],
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[AdmissionGQLModel]]:
        result = await Delete[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
        return result

