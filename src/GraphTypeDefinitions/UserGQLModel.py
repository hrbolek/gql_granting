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

from .BaseGQLModel import IDType, resolve_reference

StudentGQLModel = typing.Annotated["StudentGQLModel", strawberry.lazy(".Student")]
StudentInputFilter = typing.Annotated["StudentInputFilter", strawberry.lazy(".Student")]

@strawberry.federation.type(
    extend=True,
    keys=["id"]
)
class UserGQLModel:

    id: IDType = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    studies: typing.List["StudentGQLModel"] = strawberry.field(
        description="studies, aka what user is studying (with state)",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver["StudentGQLModel"](fkey_field_name="user_id", whereType=StudentInputFilter)
    )