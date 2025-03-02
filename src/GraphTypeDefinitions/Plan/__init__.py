import strawberry

from .EvaluationGQLModel import EvaluationQuery, EvaluationMutation
from .ExamGQLModel import ExamGQLModel, ExamQuery, ExamMutation
from .StudyPlanGQLModel import StudyPlanQuery, StudyPlanMutation
from. StudyPlanLessonGQLModel import StudyPlanLessonQuery, StudyPlanLessonMutation



@strawberry.interface
class PlanQuery(
    EvaluationQuery,
    ExamQuery,
    StudyPlanQuery,
    StudyPlanLessonQuery
):
    pass


@strawberry.interface
class PlanMutation(
    EvaluationMutation,
    ExamMutation,
    StudyPlanMutation,
    StudyPlanLessonMutation
):
    pass