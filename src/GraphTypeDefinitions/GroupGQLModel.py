import typing
import strawberry
import strawberry.types


from uoishelpers.resolvers import (
    ScalarResolver,
    VectorResolver,

    createInputs2
)
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)

from .BaseGQLModel import IDType, resolve_reference
from .Program import ProgramGQLModel
from .Program.SubjectGQLModel import SubjectInputFilter, SubjectGQLModel

@createInputs2
class GroupProgramsInputFilter:
    from .Program.ProgramGQLModel import ProgramInputFilter
    programs: ProgramInputFilter

@createInputs2
class GroupSubjectsInputFilter:
    from .Program.SubjectGQLModel import SubjectInputFilter
    subjects: SubjectInputFilter

@strawberry.federation.type(
    extend=True,
    keys=["id"]
)
class GroupGQLModel:

    id: IDType = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    accredited_programs: typing.List[ProgramGQLModel] = strawberry.field(
        description="List of accredited study programs that are implemented (offered and delivered) by this organizational unit (typically a faculty).",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[ProgramGQLModel](fkey_field_name="licenced_group_id", whereType=GroupProgramsInputFilter)
    )

    accredited_subjects: typing.List[SubjectGQLModel] = strawberry.field(
        description="List of accredited study programs that are implemented (offered and delivered) by this organizational unit (typically a faculty).",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[SubjectGQLModel](fkey_field_name="group_id", whereType=GroupSubjectsInputFilter)
    )
    # @strawberry.field(
    #     description="List of accredited study programs that are implemented (offered and delivered) by this organizational unit (typically a faculty).",
    #     permission_classes=[OnlyForAuthentized]
    # )
    # async def accredited_programs(self, info: strawberry.types.Info) -> typing.List[ProgramGQLModel]:
    #     from .Program.ProgramGQLModel import ProgramGQLModel
    #     loader = ProgramGQLModel.getLoader(info=)