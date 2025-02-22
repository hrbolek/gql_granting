import strawberry

from .ProgramGQLModel import ProgramGQLModel, ProgramQuery as _ProgramQuery, ProgramMutation as _ProgramMutation
from .LessonGQLModel import LessonQuery

from .ProgramFormTypeGQLModel import ProgramFormQuery
from .ProgramLanguageTypeGQLModel import ProgramLanguageQuery
from .ProgramLevelTypeGQLModel import ProgramLevelQuery
from .ProgramTitleTypeGQLModel import ProgramTitleQuery
from .ProgramTypeGQLModel import ProgramTypeQuery

from .SemesterGQLModel import SemesterQuery, SemesterMutation
from .SubjectGQLModel import SubjectQuery, SubjectMutation
from .TopicGQLModel import TopicQuery, TopicMutation

@strawberry.interface(name="ProgramAllQuery")
class ProgramQuery(
    _ProgramQuery,
    ProgramFormQuery,
    ProgramLanguageQuery,
    ProgramLevelQuery,
    ProgramTitleQuery,
    ProgramTypeQuery,

    SemesterQuery,
    SubjectQuery,
    TopicQuery
):
    pass

@strawberry.interface(name="ProgramAllMutation")
class ProgramMutation(
    _ProgramMutation
):
    pass
