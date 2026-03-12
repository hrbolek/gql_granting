import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs2,

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

from ..BaseGQLModel import BaseGQLModel, IDType


ProgramLevelTypeGQLModel = typing.Annotated["ProgramLevelTypeGQLModel", strawberry.lazy(".ProgramLevelTypeGQLModel")]
ProgramTitleTypeGQLModel = typing.Annotated["ProgramTitleTypeGQLModel", strawberry.lazy(".ProgramTitleTypeGQLModel")]
ProgramLanguageTypeGQLModel = typing.Annotated["ProgramLanguageTypeGQLModel", strawberry.lazy(".ProgramLanguageTypeGQLModel")]
ProgramFormTypeGQLModel = typing.Annotated["ProgramFormTypeGQLModel", strawberry.lazy(".ProgramFormTypeGQLModel")]


@createInputs2
class ProgramTypeInputFilter:
    id: IDType
    name: str
    name_en: str
    level_id: IDType
    title_id: IDType
    language_id: IDType
    form_id: IDType
    # from .ProgramLevelTypeGQLModel import ProgramLevelTypeInputFilter
    # level: ProgramLevelTypeInputFilter


@strawberry.federation.type(
    description="Unites attributes into single type",
    keys=["id"]
)
class ProgramTypeGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info=info).ProgramTypeModel

    name: typing.Optional[str] = strawberry.field(
        description="name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="english name",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    level_id: typing.Optional[IDType] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    level_type: typing.Optional["ProgramLevelTypeGQLModel"] = strawberry.field(
        description="level of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramLevelTypeGQLModel](fkey_field_name="level_id")
    )

    title_id: typing.Optional[IDType] = strawberry.field(
        description="title given to student",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    title_type: typing.Optional["ProgramTitleTypeGQLModel"] = strawberry.field(
        description="title given to student",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramTitleTypeGQLModel](fkey_field_name="title_id")
    )    

    language_id: typing.Optional[IDType] = strawberry.field(
        description="language used in programme",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    language_type: typing.Optional["ProgramLanguageTypeGQLModel"] = strawberry.field(
        description="language used in programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramLanguageTypeGQLModel](fkey_field_name="language_id")
    )        

    form_id: typing.Optional[IDType] = strawberry.field(
        description="teaching form, like presential, distance, etc.",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    form_type: typing.Optional["ProgramFormTypeGQLModel"] = strawberry.field(
        description="teaching form, like presential, distance, etc.",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[ProgramFormTypeGQLModel](fkey_field_name="form_id")
    )        


@strawberry.interface(
    description=""
)
class ProgramTypeQuery:
    program_type_by_id: typing.Optional["ProgramTypeGQLModel"] = strawberry.field(
        description="returns programtype by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramTypeGQLModel.load_with_loader
    )

    program_type_page: typing.List["ProgramTypeGQLModel"] = strawberry.field(
        description="returns programtypes defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramTypeGQLModel"](whereType=ProgramTypeInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class ProgramTypeInsertGQLModel(InputModelMixin):
    getLoader = ProgramTypeGQLModel.getLoader
    id: typing.Optional[IDType] = strawberry.field(description="primary key client generated", default=None)
    name: typing.Optional[str] = strawberry.field(description="name of the program_type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name of the program_type", default=None)
    level_id: typing.Optional[IDType] = strawberry.field(description="level of programme", default=None)
    title_id: typing.Optional[IDType] = strawberry.field(description="title given to student", default=None)
    language_id: typing.Optional[IDType] = strawberry.field(description="language used in programme", default=None)
    form_id: typing.Optional[IDType] = strawberry.field(description="teaching form, like presential, distance, etc.", default=None)

    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class ProgramTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(description="name of the program_type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="name of the program_type", default=None)
    level_id: typing.Optional[IDType] = strawberry.field(description="level of programme", default=None)
    title_id: typing.Optional[IDType] = strawberry.field(description="title given to student", default=None)
    language_id: typing.Optional[IDType] = strawberry.field(description="language used in programme", default=None)
    form_id: typing.Optional[IDType] = strawberry.field(description="teaching form, like presential, distance, etc.", default=None)

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description=""
)
class ProgramTypeMutation:

    @strawberry.mutation(
        description="create a new program_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, ProgramTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_type_insert(
        self, 
        info: strawberry.types.Info, 
        program_type: ProgramTypeInsertGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramTypeGQLModel, InsertError[ProgramTypeGQLModel]]:
        return await Insert[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        
    
    @strawberry.mutation(
        description="updates existing program_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, ProgramTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_type_update(
        self, 
        info: strawberry.types.Info, 
        program_type: ProgramTypeUpdateGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Union[ProgramTypeGQLModel, UpdateError[ProgramTypeGQLModel]]:
        return await Update[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        

    @strawberry.mutation(
        description="delete existing program_type",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, ProgramTypeGQLModel](
                roles=[
                    # "administrátor", 
                    "superadmin"
                ]
            ),
        ],
    )
    async def program_type_delete(
        self, 
        info: strawberry.types.Info, 
        program_type: ProgramTypeDeleteGQLModel,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[ProgramTypeGQLModel]]:
        return await Delete[ProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
        

