import typing
import strawberry
import strawberry.types


from uoishelpers.resolvers import (
    ScalarResolver
)
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)

from .BaseGQLModel import IDType, resolve_reference
from .Program import ProgramGQLModel

@strawberry.federation.type(
    extend=True,
    keys=["id"]
)
class GroupGQLModel:

    id: IDType = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    accredited_programs: typing.Optional[ProgramGQLModel] = strawberry.field(
        description="List of accredited study programs that are implemented (offered and delivered) by this organizational unit (typically a faculty).",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[ProgramGQLModel](f_key_field_name="licenced_group_id")
    )