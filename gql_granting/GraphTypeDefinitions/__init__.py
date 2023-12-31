import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .AcLessonGQLModel import aclesson_by_id
    aclesson_by_id = aclesson_by_id

    from .AcLessonGQLModel import aclesson_type_page
    aclesson_type_page = aclesson_type_page

    from .AcClassificationGQLModel import acclassification_page
    acclassification_page = acclassification_page

    from .AcClassificationGQLModel import acclassification_page_by_user
    acclassification_page_by_user = acclassification_page_by_user

    from .AcProgramGQLModel import program_by_id
    program_by_id = program_by_id

    from .AcProgramGQLModel import program_page 
    program_page = program_page 

    from .AcSemesterGQLModel import acsemester_page
    acsemester_page = acsemester_page 

    from .AcSubjectGQLModel import acsubject_by_id
    acsubject_by_id = acsubject_by_id 

    from .AcSubjectGQLModel import acsubject_page
    acsubject_page = acsubject_page

    from .AcTopicGQLModel import actopic_by_id 
    actopic_by_id = actopic_by_id
    
    pass
    
@strawberry.type
class Mutation:
    from .AcClassificationGQLModel import classification_insert
    classification_insert = classification_insert

    from .AcProgramGQLModel import program_insert
    program_insert = program_insert 

    from .AcClassificationGQLModel import classification_update 
    classification_update= classification_update 

    from .AcProgramGQLModel import program_update
    program_update = program_update 

    from .AcTopicGQLModel import topic_insert 
    topic_insert = topic_insert

    from .AcTopicGQLModel import topic_update 
    topic_update = topic_update 

    from .AcSubjectGQLModel import subject_insert
    subject_insert = subject_insert 

    from .AcSubjectGQLModel import subject_update
    subject_update = subject_update 

    from .AcSemesterGQLModel import semester_insert
    semester_insert = semester_insert 

    from .AcSemesterGQLModel import semester_update 
    semester_update = semester_update 

    from .AcLessonGQLModel import lesson_insert
    lesson_insert= lesson_insert 

    from .AcLessonGQLModel import lesson_update 
    lesson_update = lesson_update 

    pass

from .externals import UserGQLModel,GroupGQLModel

schema = strawberry.federation.Schema(query=Query, mutation=Mutation,types=(UserGQLModel,GroupGQLModel))