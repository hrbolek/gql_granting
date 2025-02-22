import strawberry

from .EvaluationGQLModel import EvaluationQuery, EvaluationMutation
from .ExamGQLModel import ExamGQLModel, ExamQuery
from .StudyPlanGQLModel import StudyPlanQuery
from. StudyPlanLessonGQLModel import StudyPlanLessonQuery



@strawberry.interface
class PlanQuery(
    EvaluationQuery,
    ExamQuery,
    StudyPlanQuery,
    StudyPlanLessonQuery
):
    pass