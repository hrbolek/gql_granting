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
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension

from ..BaseGQLModel import BaseGQLModel, IDType

SubjectGQLModel = typing.Annotated["SubjectGQLModel", strawberry.lazy(".SubjectGQLModel")]
SubjectInputFilter = typing.Annotated["SubjectInputFilter", strawberry.lazy(".SubjectGQLModel")]
StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy("..Student.StudentGQLModel")]
StudentInputFilter = typing.Annotated["StudentInputFilter", strawberry.lazy("..Student.StudentGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("..GroupGQLModel")]
ProgramTypeGQLModel = typing.Annotated["ProgramTypeGQLModel", strawberry.lazy(".ProgramTypeGQLModel")]

@createInputs2
class ProgramInputFilter:
    id: IDType# = strawberry.field(description="filter with operators on id field")
    name: str# = strawberry.field(description="filter with operators on name field")
    name_en: str

    licenced_group_id: IDType
    type_id: IDType
    
    # from .SubjectGQLModel import SubjectInputFilter
    subjects: SubjectInputFilter
    # from ..Student.StudentGQLModel import StudentInputFilter
    students: StudentInputFilter


@strawberry.federation.type(
    keys=["id"],
    description="""Program entity, represents an accredited study""")
class ProgramGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ProgramModel
    
    name: typing.Optional[str] = strawberry.field(
        description="Name of program",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="Eng. name of program",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    subjects: typing.List["SubjectGQLModel"] = strawberry.field(
        description="""Program subjects""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["SubjectGQLModel"](fkey_field_name="program_id", whereType=SubjectInputFilter)
    )

    students: typing.List["StudentGQLModel"] = strawberry.field(
        description="students",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudentGQLModel"](fkey_field_name="program_id", whereType=StudentInputFilter)
    )

    guarantors_group_id: typing.Optional[IDType] = strawberry.field(
        description="guarantors of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    guarantors: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="guarantors of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="guarantors_group_id")
    )

    licenced_group_id: typing.Optional[IDType] = strawberry.field(
        description="Foreign key referencing the group (e.g., faculty or department) that is officially authorized to deliver this accredited study program.",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    licenced_group: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="The group (e.g., faculty or department) that is officially authorized to deliver this accredited study program.",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["GroupGQLModel"](fkey_field_name="licenced_group_id")
    )    

    type_id: typing.Optional[IDType] = strawberry.field(
        description="type of programme",
        permission_classes=[
            OnlyForAuthentized
        ],
        default=None
    )

    type_: typing.Optional["ProgramTypeGQLModel"] = strawberry.field(
        name="type",
        description="type of pragramme",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver["ProgramTypeGQLModel"](fkey_field_name="type_id")
    )

@strawberry.interface(
    description=""
)
class ProgramQuery:
    program_by_id: typing.Optional["ProgramGQLModel"] = strawberry.field(
        description="returns program by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ProgramGQLModel.load_with_loader
    )

    program_page: typing.List["ProgramGQLModel"] = strawberry.field(
        description="returns programs defined by filter",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver["ProgramGQLModel"](whereType=ProgramInputFilter)
    )

from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="parameter for create operation"
)
class ProgramInsertGQLModel(InputModelMixin):
    getLoader = ProgramGQLModel.getLoader
    licenced_group_id: IDType = strawberry.field(
        description="who is licenced to teach", 
        # default=None
    )
    guarantors_group_id: IDType = strawberry.field(
        description="guarantors", 
        # default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="primary key client generated", 
        default=None
    )
    name: typing.Optional[str] = strawberry.field(
        description="name of the program", 
        default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the program", default=None
    )
    type_id: typing.Optional[IDType] = strawberry.field(
        description="programme type", default=None
    )
    
    from .SubjectGQLModel import SubjectInsertGQLModel
    subjects: typing.Optional[typing.List[SubjectInsertGQLModel]] = strawberry.field(
        description="subjects of the program",
        default_factory=list
    )

    rbacobject_id: strawberry.Private[IDType] = None
    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="parameter for update operation"
)
class ProgramUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")
    name: typing.Optional[str] = strawberry.field(
        description="name of the program", default=None
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="name of the program", default=None
    )
    # group_id: typing.Optional[IDType] = strawberry.field(description="guarantors", default=None)
    # licenced_group_id: typing.Optional[IDType] = strawberry.field(description="who is licenced to teach", default=None)
    type_id: typing.Optional[IDType] = strawberry.field(description="programme type", default=None)

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="parameter for delete operation"
)
class ProgramDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp for concurrent update")


@strawberry.interface(
    description="set of mutations on ProgramGQLModel"
)
class ProgramMutation:
    
    @strawberry.mutation(
        description="create a new program",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, ProgramGQLModel](
                roles=[
                    "studijní administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[InsertError, ProgramGQLModel](),
            RbacInsertProviderExtension[InsertError, ProgramGQLModel](rbac_key_name="licenced_group_id")
        ]
    )
    async def program_insert(
        self, 
        info: strawberry.types.Info, 
        program: ProgramInsertGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType
    ) -> typing.Union[ProgramGQLModel, InsertError[ProgramGQLModel]]:
        program.rbacobject_id = rbacobject_id
        return await Insert[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        
    
    @strawberry.mutation(
        description="updates existing program",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, ProgramGQLModel](
                roles=[
                    "studijní administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, ProgramGQLModel](),
            RbacProviderExtension[UpdateError, ProgramGQLModel](),
            LoadDataExtension[UpdateError, ProgramGQLModel]()
        ]
    )
    async def program_update(
        self, 
        info: strawberry.types.Info, 
        program: ProgramUpdateGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Union[ProgramGQLModel, UpdateError[ProgramGQLModel]]:
        return await Update[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        

    @strawberry.mutation(
        description="delete existing program",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, ProgramGQLModel](
                roles=[
                    "studijní administrátor", 
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, ProgramGQLModel](),
            RbacProviderExtension[DeleteError, ProgramGQLModel](),
            LoadDataExtension[DeleteError, ProgramGQLModel]()
        ]
    )
    async def program_delete(
        self, 
        info: strawberry.types.Info, 
        program: ProgramDeleteGQLModel,
        user_roles: typing.List[dict],
        rbacobject_id: IDType,
        db_row: typing.Any
    ) -> typing.Optional[DeleteError[ProgramGQLModel]]:
        return await Delete[ProgramGQLModel].DoItSafeWay(info=info, entity=program)
        

