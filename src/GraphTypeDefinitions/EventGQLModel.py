import strawberry

from .BaseGQLModel import IDType, resolve_reference

@strawberry.federation.type(
    extend=True,
    keys=["id"]
)
class EventGQLModel:

    id: IDType = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference
