import strawberry
from .BaseGQLModel import IDType


from .Program import ProgramQuery
from .Student import StudentQuery
@strawberry.type(description="""Type for query root""")
class Query(ProgramQuery, StudentQuery):
    pass

from .Program import ProgramMutation
@strawberry.type(description="root of mutations")
class Mutation(ProgramMutation):
    pass

schema = strawberry.federation.Schema(
    query=Query,
    # mutation=Mutation,
    extensions=[],
    types=[]
)

from uoishelpers.schema import WhoAmIExtension
schema.extensions.append(WhoAmIExtension)