import strawberry

from .ProgramGQLModel import ProgramGQLModel, ProgramQuery as _ProgramQuery, ProgramMutation as _ProgramMutation
from .LessonGQLModel import LessonQuery

from .ProgramFormTypeGQLModel import ProgramFormTypeQuery, ProgramFormTypeMutation
from .ProgramLanguageTypeGQLModel import ProgramLanguageQuery, ProgramLanguageTypeMutation
from .ProgramLevelTypeGQLModel import ProgramLevelQuery, ProgramLevelTypeMutation
from .ProgramTitleTypeGQLModel import ProgramTitleQuery, ProgramTitleTypeMutation
from .ProgramTypeGQLModel import ProgramTypeQuery, ProgramTypeMutation

from .SemesterGQLModel import SemesterQuery, SemesterMutation
from .SubjectGQLModel import SubjectQuery, SubjectMutation
from .TopicGQLModel import TopicQuery, TopicMutation
from .LessonGQLModel import LessonGQLModel, LessonMutation, LessonQuery
from .LessonTypeGQLModel import LessonTypeGQLModel, LessonTypeMutation, LessonTypeQuery

from .ClassificationTypeGQLModel import ClassificationTypeGQLModel, ClassificationTypeQueries, ClassificationTypeMutations
from .ClassificationLevelGQLModel import ClassificationLevelGQLModel, ClassificationLevelQueries, ClassificationLevelMutations

@strawberry.interface(name="ProgramAllQuery")
class ProgramQuery(
    _ProgramQuery,
    ProgramFormTypeQuery,
    ProgramLanguageQuery,
    ProgramLevelQuery,
    ProgramTitleQuery,
    ProgramTypeQuery,

    SemesterQuery,
    SubjectQuery,
    TopicQuery,

    LessonQuery,
    LessonTypeQuery,

    ClassificationTypeQueries,
    ClassificationLevelQueries
):
    pass

@strawberry.interface(name="ProgramAllMutation")
class ProgramMutation(
    _ProgramMutation,
    ProgramFormTypeMutation,
    ProgramLanguageTypeMutation,
    ProgramLevelTypeMutation,
    ProgramTitleTypeMutation,
    ProgramTypeMutation,
    SemesterMutation,
    SubjectMutation,
    TopicMutation,
    
    LessonMutation,
    LessonTypeMutation,

    ClassificationTypeMutations,
    ClassificationLevelMutations
):
    pass
