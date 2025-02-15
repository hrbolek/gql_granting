# GraphQL API Documentation

## _Any

No description available.


---
## Query

No description available.

### Fields:

- **_entities** (`List[_Entity]!`): 

    No description available.
- **_service** (`_Service!`): 

    No description available.
- **programById** (`ProgramGQLModel`): 

    returns program by its id
- **programPage** (`List[ProgramGQLModel!]!`): 

    returns programs defined by filter
- **hello** (`String!`): 

    No description available.

---
## ProgramQuery

No description available.

### Fields:

- **programById** (`ProgramGQLModel`): 

    returns program by its id
- **programPage** (`List[ProgramGQLModel!]!`): 

    returns programs defined by filter

---
## ProgramGQLModel

Program entity

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **subjects** (`List[SubjectGQLModel!]!`): 

    Program subjects
- **students** (`List[StudentGQLModel!]!`): 

    students
- **guarantorsId** (`UUID`): 

    guarantors of programme
- **guarantors** (`GroupGQLModel`): 

    guarantors of programme
- **licensedId** (`UUID`): 

    Who has got license for programme
- **licensed** (`GroupGQLModel`): 

    Who has got license for programme
- **typeId** (`UUID`): 

    type of programme
- **type** (`ProgramTypeGQLModel`): 

    type of pragramme

---
## BaseGQLModel

Entity representing an interface

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user

---
## UUID

No description available.


---
## Date

Date (isoformat)


---
## UserGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.
- **studies** (`StudentGQLModel`): 

    studies, aka what user is studying (with state)

---
## StudentGQLModel

No description available.

### Fields:

- **userId** (`UUID`): 

    No description available.
- **user** (`UserGQLModel`): 

    who is student
- **programId** (`UUID`): 

    No description available.
- **program** (`ProgramGQLModel`): 

    which program student is studying
- **stateId** (`UUID`): 

    No description available.
- **state** (`StateGQLModel`): 

    State of the user study
- **evaluations** (`List[EvaluationGQLModel!]!`): 

    given grades

---
## StateGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.

---
## EvaluationGQLModel

Exam evaluation

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **points** (`Int`): 

    given points for this exam
- **grade** (`String`): 

    given grade / mark
- **attempt** (`Int`): 

    index of attempt
- **passed** (`Boolean`): 

    True if student passed this exam
- **studentId** (`UUID`): 

    id of the student
- **student** (`StudentGQLModel`): 

    student who is examined
- **examinerId** (`UUID`): 

    who examined
- **examiner** (`UserGQLModel`): 

    Who examined
- **semesterId** (`UUID`): 

    to which semester / subject this examination belongs
- **semester** (`SemesterGQLModel`): 

    semester to which this examination belongs to
- **examId** (`UUID`): 

    related exam conditions
- **exam** (`ExamGQLModel`): 

    related exam conditions
- **examEventId** (`UUID`): 

    No description available.
- **examEvent** (`EventGQLModel`): 

    No description available.
- **parentId** (`UUID`): 

    id of exam which this is part
- **parent** (`EvaluationGQLModel`): 

    exam of which is this part
- **children** (`List[EvaluationGQLModel!]!`): 

    sub parts of this evaluation

---
## RBACObjectGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.

---
## Int

The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.


---
## String

The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.


---
## Boolean

The `Boolean` scalar type represents `true` or `false`.


---
## SemesterGQLModel

Semester entity

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **credits** (`Int`): 

    credits
- **subjectId** (`UUID`): 

    subject id
- **subject** (`SubjectGQLModel`): 

    subject
- **topics** (`List[TopicGQLModel!]!`): 

    Semester topics
- **plans** (`List[StudyPlanGQLModel!]!`): 

    plans of study execution

---
## SubjectGQLModel

Subject entity

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String!`): 

    subject name
- **nameEn** (`String!`): 

    subject name in english
- **programId** (`UUID!`): 

    program id
- **program** (`ProgramGQLModel`): 

    program entity
- **semesters** (`List[SemesterGQLModel!]!`): 

    subject semesters
- **guarantorsId** (`UUID`): 

    guarantors of programme
- **guarantors** (`GroupGQLModel`): 

    guarantors of programme

---
## SemesterInputFilter

Operators definition on SemesterInputFilter


---
## SemesterInputFilterOr

Or operator definition on SemesterInputFilter


---
## SemesterInputFilterAnd

And operator definition on SemesterInputFilter


---
## UuidFilter

Integer filter methods, only one constrain allowed


---
## StrFilter

Str filter methods, only one constrain allowed


---
## GroupGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.

---
## TopicGQLModel

Topic entity

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    topic name
- **description** (`String`): 

    topic description
- **semesterId** (`UUID`): 

    semester id
- **semester** (`SemesterGQLModel`): 

    semester
- **lessons** (`List[LessonGQLModel!]!`): 

    lessons

---
## LessonGQLModel

Lesson entity

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **topicId** (`UUID`): 

    No description available.
- **topic** (`TopicGQLModel`): 

    No description available.

---
## LessonInputFilter

Operators definition on LessonInputFilter


---
## LessonInputFilterOr

Or operator definition on LessonInputFilter


---
## LessonInputFilterAnd

And operator definition on LessonInputFilter


---
## TopicInputFilter

Operators definition on TopicInputFilter


---
## TopicInputFilterOr

Or operator definition on TopicInputFilter


---
## TopicInputFilterAnd

And operator definition on TopicInputFilter


---
## StudyPlanGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **semesterId** (`UUID`): 

    ID of Semester to which the plan is related
- **semester** (`SemesterGQLModel`): 

    Semester to which the plan is related
- **lessons** (`List[StudyPlanLessonGQLModel!]!`): 

    part of study plan
- **examId** (`UUID`): 

    Exam Rules
- **exam** (`ExamGQLModel`): 

    Exam Rules
- **eventId** (`UUID`): 

    Time period when the plan will live
- **event** (`EventGQLModel`): 

    Time period when the plan will live

---
## StudyPlanLessonGQLModel

On row in studyplan

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **order** (`Int`): 

    order in plan
- **length** (`Int`): 

    length in fictive units
- **eventId** (`UUID`): 

    id of event which has been planed for this lesson
- **event** (`EventGQLModel`): 

    event which has been planed for this lesson
- **topicId** (`UUID`): 

    Topic to which the Lesson is related
- **topic** (`TopicGQLModel`): 

    Topic to which the Lesson is related
- **linkedWithId** (`UUID`): 

    No description available.
- **linkedWith** (`List[StudyPlanLessonGQLModel!]!`): 

    list of linked othe planned lessons
- **instructors** (`List[UserGQLModel!]!`): 

    whos teach the lesson
- **studyGroups** (`List[GroupGQLModel!]!`): 

    study groups
- **facilities** (`List[FacilityGQLModel!]!`): 

    places for this lesson

---
## EventGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.

---
## FacilityGQLModel

No description available.

### Fields:

- **id** (`UUID!`): 

    No description available.

---
## StudyPlanLessonInputFilter

Operators definition on StudyPlanLessonInputFilter


---
## StudyPlanLessonInputFilterOr

Or operator definition on StudyPlanLessonInputFilter


---
## StudyPlanLessonInputFilterAnd

And operator definition on StudyPlanLessonInputFilter


---
## ExamGQLModel

Exam definition

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    No description available.
- **description** (`String`): 

    extended description of exam conditions
- **minScore** (`Int`): 

    defined minimum points to pass the exam
- **maxScore** (`Int`): 

    defined maximum achievable points
- **parentId** (`UUID`): 

    id of exam which is part
- **parent** (`UUID`): 

    exam is part of exam
- **parts** (`List[ExamGQLModel!]!`): 

    exam parts
- **evaluations** (`List[EvaluationGQLModel!]!`): 

    evaluations of users during exams

---
## ExamInputFilter

Operators definition on ExamInputFilter


---
## ExamInputFilterOr

Or operator definition on ExamInputFilter


---
## ExamInputFilterAnd

And operator definition on ExamInputFilter


---
## EvaluationInputFilter

Operators definition on EvaluationInputFilter


---
## EvaluationInputFilterOr

Or operator definition on EvaluationInputFilter


---
## EvaluationInputFilterAnd

And operator definition on EvaluationInputFilter


---
## DatetimeFilter

Datetime filter methods, only one constrain allowed


---
## DateTime

Date with time (isoformat)


---
## IntFilter

Integer filter methods, only one constrain allowed


---
## StudyPlanInputFilter

Operators definition on StudyPlanInputFilter


---
## StudyPlanInputFilterOr

Or operator definition on StudyPlanInputFilter


---
## StudyPlanInputFilterAnd

And operator definition on StudyPlanInputFilter


---
## StudentInputFilter

Operators definition on StudentInputFilter


---
## StudentInputFilterOr

Or operator definition on StudentInputFilter


---
## StudentInputFilterAnd

And operator definition on StudentInputFilter


---
## SubjectInputFilter

Operators definition on SubjectInputFilter


---
## SubjectInputFilterOr

Or operator definition on SubjectInputFilter


---
## SubjectInputFilterAnd

And operator definition on SubjectInputFilter


---
## ProgramTypeGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    name
- **nameEn** (`String`): 

    english name
- **levelTypeId** (`UUID`): 

    level of programme
- **levelType** (`ProgramLevelTypeGQLModel`): 

    level of programme
- **titleTypeId** (`UUID`): 

    level of programme
- **titleType** (`ProgramTitleTypeGQLModel`): 

    level of programme
- **languageTypeId** (`UUID`): 

    level of programme
- **languageType** (`ProgramLanguageTypeGQLModel`): 

    level of programme
- **formTypeId** (`UUID`): 

    level of programme
- **formType** (`ProgramFormTypeGQLModel`): 

    level of programme

---
## ProgramLevelTypeGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    name
- **nameEn** (`String`): 

    english name

---
## ProgramTitleTypeGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    name
- **nameEn** (`String`): 

    english name

---
## ProgramLanguageTypeGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    name
- **nameEn** (`String`): 

    english name

---
## ProgramFormTypeGQLModel

No description available.

### Fields:

- **id** (`UUID`): 

    primary key
- **lastchange** (`Date`): 

    timestamp
- **created** (`Date`): 

    date & time of unit born
- **createdbyId** (`UUID`): 

    who created this entity
- **changedbyId** (`UUID`): 

    who changed this entity
- **rbacobjectId** (`UUID`): 

    rbac ruling object
- **createdby** (`UserGQLModel`): 

    who created this entity
- **changedby** (`UserGQLModel`): 

    who created this entity
- **rbacobject** (`RBACObjectGQLModel`): 

    rbac holds relations of user
- **name** (`String`): 

    name
- **nameEn** (`String`): 

    english name

---
## ProgramInputFilter

Operators definition on ProgramInputFilter


---
## ProgramInputFilterOr

Or operator definition on ProgramInputFilter


---
## ProgramInputFilterAnd

And operator definition on ProgramInputFilter


---
## _Entity

No description available.


---
## _Service

No description available.

### Fields:

- **sdl** (`String!`): 

    No description available.

---
