import strawberry

from .Plan import PlanQuery, PlanMutation
from .Program import (
    ProgramQuery, 
    ProgramMutation,
    LessonGQLModel,
    LessonTypeGQLModel
)
from .Admission import (
    AdmissionQuery, 
    AdmissionMutation, 
    PaymentQuery, 
    PaymentMutation, 
    PaymentInfoQuery, 
    PaymentInfoMutation
)
from .Student import StudentQuery, StudentMutation

@strawberry.type(description="""Type for query root""")
class Query(
    ProgramQuery, 
    StudentQuery, 
    PlanQuery,

    AdmissionQuery,
    PaymentQuery,
    PaymentInfoQuery
):
    pass

@strawberry.type(description="root of mutations")
class Mutation(
    ProgramMutation,
    StudentMutation,
    PlanMutation,

    AdmissionMutation,
    PaymentMutation,
    PaymentInfoMutation
):
    pass