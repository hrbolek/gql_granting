
from typing import TypedDict, Optional, List, Any, Annotated
import uuid
import datetime


class StudentInputFilter(TypedDict, total=False):


    # Filter method
    _or: Optional[List["StudentInputFilterOr"]]

    # Filter method
    _and: Optional[List["StudentInputFilterAnd"]]

    # Filter method
    id: Optional["UuidFilter"]

    # Filter method
    user_id: Optional["UuidFilter"]

    # Filter method
    program_id: Optional["UuidFilter"]

    # Filter method
    semester_number: Optional["IntFilter"]

    # Filter method
    state_id: Optional["UuidFilter"]




class StudentInputFilterOr(TypedDict, total=False):


    # Filter method
    _and: Optional[List["StudentInputFilterAnd"]]

    # Filter method
    id: Optional["UuidFilter"]

    # Filter method
    user_id: Optional["UuidFilter"]

    # Filter method
    program_id: Optional["UuidFilter"]

    # Filter method
    semester_number: Optional["IntFilter"]

    # Filter method
    state_id: Optional["UuidFilter"]




class StudentInputFilterAnd(TypedDict, total=False):


    # Filter method
    _or: Optional[List["StudentInputFilterOr"]]

    # Filter method
    id: Optional["UuidFilter"]

    # Filter method
    user_id: Optional["UuidFilter"]

    # Filter method
    program_id: Optional["UuidFilter"]

    # Filter method
    semester_number: Optional["IntFilter"]

    # Filter method
    state_id: Optional["UuidFilter"]




class UuidFilter(TypedDict, total=False):


    # operation for select.filter() method
    _eq: Optional[uuid.UUID]

    # operation for select.filter() method
    _in: Optional[List[uuid.UUID]]




class IntFilter(TypedDict, total=False):


    # operation for select.filter() method
    _eq: Optional[int]

    # operation for select.filter() method
    _le: Optional[int]

    # operation for select.filter() method
    _lt: Optional[int]

    # operation for select.filter() method
    _ge: Optional[int]

    # operation for select.filter() method
    _gt: Optional[int]

    # operation for select.filter() method
    _in: Optional[List[int]]






from typing import TypedDict, Optional, List, Any, Annotated
import uuid
import datetime


class StudentGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # id of the user
    userId: Optional[uuid.UUID]

    # who is student
    student: Optional[Any]

    # the program which user is studying
    programId: Optional[uuid.UUID]

    # which program student is studying
    program: Optional["ProgramGQLModel"]

    # in what state the student is
    stateId: Optional[uuid.UUID]

    # semester of study
    semesterNumber: Optional[int]

    # State of the user study
    state: Optional[Any]

    # given grades
    evaluations: List["EvaluationGQLModel"]




class ProgramGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # Name of program
    name: Optional[str]

    # Eng. name of program
    nameEn: Optional[str]

    # Program subjects
    subjects: List["SubjectGQLModel"]

    # students
    students: List["StudentGQLModel"]

    # guarantors of programme
    groupId: Optional[uuid.UUID]

    # guarantors of programme
    guarantors: Optional[Any]

    # Foreign key referencing the group (e.g., faculty or department) that is officially authorized to deliver this accredited study program.
    licencedGroupId: Optional[uuid.UUID]

    # The group (e.g., faculty or department) that is officially authorized to deliver this accredited study program.
    licencedGroup: Optional[Any]

    # type of programme
    typeId: Optional[uuid.UUID]

    # type of pragramme
    type: Optional["ProgramTypeGQLModel"]




class SubjectGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # subject name
    name: Optional[str]

    # subject name in english
    nameEn: Optional[str]

    # subject description
    description: Optional[str]

    # subject description in english
    descriptionEn: Optional[str]

    # program id
    programId: Optional[uuid.UUID]

    # program entity
    program: Optional["ProgramGQLModel"]

    # subject semesters
    semesters: List["SemesterGQLModel"]

    # guarantors of programme
    groupId: Optional[uuid.UUID]

    # guarantors of programme
    guarantors: Optional[Any]




class SemesterGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # order in same subject
    order: Optional[int]

    # True if every student must pass this subject
    mandatory: Optional[bool]

    # credits
    credits: Optional[int]

    # subject id
    classificationtypeId: Optional[uuid.UUID]

    # subject id
    subjectId: Optional[uuid.UUID]

    # subject
    subject: Optional["SubjectGQLModel"]

    # subjects vhcin must be studied at first
    prerequisites: List["SubjectGQLModel"]

    # Semester topics
    topics: List["TopicGQLModel"]

    # plans of study execution
    plans: List["StudyPlanGQLModel"]




class TopicGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # topic name
    name: Optional[str]

    # topic name
    nameEn: Optional[str]

    # topic name
    order: Optional[int]

    # topic description
    description: Optional[str]

    # semester id
    semesterId: Optional[uuid.UUID]

    # semester
    semester: Optional["SemesterGQLModel"]

    # lessons
    lessons: List["LessonGQLModel"]




class LessonGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # how many virtual time units
    count: Optional[int]

    # to which topic belongs
    topicId: Optional[uuid.UUID]

    # to which topic belongs
    topic: Optional["TopicGQLModel"]

    # type of Lesson, like Laboratories
    typeId: Optional[uuid.UUID]

    # type of Lesson, like Laboratories
    type: Optional["LessonTypeGQLModel"]




class LessonTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]

    # abbreviation
    abbr: Optional[str]




class StudyPlanGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # ID of Semester to which the plan is related
    semesterId: Optional[uuid.UUID]

    # Semester to which the plan is related
    semester: Optional["SemesterGQLModel"]

    # ID of classification conditions
    examId: Optional[uuid.UUID]

    # part of study plan
    lessons: List["StudyPlanLessonGQLModel"]

    # Exam Rules
    exam: Optional["ExamGQLModel"]

    # Time period when the plan will live
    eventId: Optional[uuid.UUID]

    # Time period when the plan will live
    event: Optional[Any]




class StudyPlanLessonGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # order in plan
    order: Optional[int]

    # lesson name
    name: Optional[str]

    # lesson name in english
    nameEn: Optional[str]

    # length in fictive units
    length: Optional[int]

    # id of event which has been planed for this lesson
    eventId: Optional[uuid.UUID]

    # event which has been planed for this lesson
    event: Optional[Any]

    # Topic to which the Lesson is related
    topicId: Optional[uuid.UUID]

    # Topic to which the Lesson is related
    topic: Optional["TopicGQLModel"]

    # Lesson type
    lessontypeId: Optional[uuid.UUID]

    # type of the lesson
    lessontype: Optional["LessonTypeGQLModel"]

    # key to describe integration with other planned lessons
    linkedWithId: Optional[uuid.UUID]

    # Plan which owns this lesson
    planId: Optional[uuid.UUID]

    # the plan to which this lesson belongs
    plan: Optional["StudyPlanGQLModel"]

    # list of linked othe planned lessons
    linkedWith: List["StudyPlanLessonGQLModel"]

    # whos teach the lesson
    instructors: List[Any]

    # study groups
    studyGroups: List[Any]

    # places for this lesson
    facilities: List[Any]




class ExamGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name of Exam, something like test 1
    name: Optional[str]

    # English name of Exam, something like test 1
    nameEn: Optional[str]

    # extended description of exam conditions
    description: Optional[str]

    # extended description of exam conditions
    descriptionEn: Optional[str]

    # defined minimum points to pass the exam
    minScore: Optional[int]

    # defined maximum achievable points
    maxScore: Optional[int]

    # id of exam type
    typeId: Optional[uuid.UUID]

    # type of classification
    type: Optional["ClassificationTypeGQLModel"]

    # id of exam which is part
    parentId: Optional[uuid.UUID]

    # exam is part of exam
    parent: Optional["ExamGQLModel"]

    # exam parts
    parts: List["ExamGQLModel"]

    # evaluations of users during exams
    evaluations: List["EvaluationGQLModel"]

    # study plan which the exam belongs to
    planId: Optional[uuid.UUID]

    # study plan which the exam belongs to
    plan: Optional["StudyPlanGQLModel"]




class ClassificationTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # the name
    name: Optional[str]

    # the name
    nameEn: Optional[str]




class EvaluationGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # index of attempt
    order: Optional[int]

    # given points for this exam
    points: Optional[int]

    # True if student passed this exam
    passed: Optional[bool]

    # description given to student and exam
    description: Optional[str]

    # given grade / mark
    grade: Optional[str]

    # id of the student
    studentId: Optional[uuid.UUID]

    # student who is examined
    student: Optional["StudentGQLModel"]

    # who examined
    examinerId: Optional[uuid.UUID]

    # Who examined
    examiner: Optional[Any]

    # to which semester / subject this examination belongs
    semesterId: Optional[uuid.UUID]

    # semester to which this examination belongs to
    semester: Optional["SemesterGQLModel"]

    # Exam plan
    examId: Optional[uuid.UUID]

    # related exam conditions
    exam: Optional["ExamGQLModel"]

    # the event when exam happened and evaluation has been stored
    eventId: Optional[uuid.UUID]

    # the event when exam happened and evaluation has been stored
    event: Optional[Any]

    # id of exam which this is part
    parentId: Optional[uuid.UUID]

    # exam of which is this part
    parent: Optional["EvaluationGQLModel"]

    # sub parts of this evaluation
    parts: List["EvaluationGQLModel"]

    # Formal given grade
    classificationlevelId: Optional[uuid.UUID]




class ProgramTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]

    # level of programme
    levelId: Optional[uuid.UUID]

    # level of programme
    levelType: Optional["ProgramLevelTypeGQLModel"]

    # title given to student
    titleId: Optional[uuid.UUID]

    # title given to student
    titleType: Optional["ProgramTitleTypeGQLModel"]

    # language used in programme
    languageId: Optional[uuid.UUID]

    # language used in programme
    languageType: Optional["ProgramLanguageTypeGQLModel"]

    # teaching form, like presential, distance, etc.
    formId: Optional[uuid.UUID]

    # teaching form, like presential, distance, etc.
    formType: Optional["ProgramFormTypeGQLModel"]




class ProgramLevelTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]

    # how many years for standard study
    length: Optional[int]

    # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D., etc.
    priority: Optional[int]




class ProgramTitleTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]




class ProgramLanguageTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]




class ProgramFormTypeGQLModel(TypedDict, total=False):


    # primary key
    id: uuid.UUID

    # timestamp
    lastchange: Optional[datetime.datetime]

    # date & time of unit born
    created: Optional[datetime.datetime]

    # who created this entity
    createdbyId: Optional[uuid.UUID]

    # who changed this entity
    changedbyId: Optional[uuid.UUID]

    # rbac ruling object
    rbacobjectId: Optional[uuid.UUID]

    # who created this entity
    createdby: Optional[Any]

    # who created this entity
    changedby: Optional[Any]

    # rbac holds relations of user
    rbacobject: Optional[Any]

    # name
    name: Optional[str]

    # english name
    nameEn: Optional[str]






from semantic_kernel.functions import kernel_function
import requests
import json

@kernel_function(
    # description="Automaticaly generated skill for acces to graphql endpoint from sdl for Query.studentPage."
)
def studentPage(
    skip: Annotated[int, "how many entities will be ignored"] = 0,
    limit: Annotated[int, "how many entities will be taken"] = 10,
    orderby: Annotated[str, "name of field which will determite the order"] = None,
    where: Annotated["StudentInputFilter", "filter"] = None, 
    context: dict = None
) -> List["StudentGQLModel"]:
    """
    Automaticaly generated skill for acces to graphql endpoint from sdl for Query.studentPage.
    returns students defined by filter
    

    Parameters:
    
    - skip (int), optional: how many entities will be ignored
    
    - limit (int), optional: how many entities will be taken
    
    - orderby (str), optional: name of field which will determite the order
    
    - where ("StudentInputFilter"), optional: filter
    
    Returns: List["StudentGQLModel"]
    """
    endpoint = ""
    query = """
    studentPage(...)
    """
    variables = {
        "skip": skip, "limit": limit, "orderby": orderby, "where": where
    }
    response = requests.post(endpoint, json={"query": query, "variables": variables})
    response.raise_for_status()
    rows = response.json()
    assert "data" in rows, f"the response does not contain the data key {rows}"
    data = rows["data"]
    return [StudentGQLModel (**x) for x in data["studentPage"]]
    # return List["StudentGQLModel"](**response.json()["data"]["studentPage"])