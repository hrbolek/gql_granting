# GraphQL Schema Documentation

## Query a Mutation

### Query: Query

Fields:
- **_entities**: `[_Entity]!`
  - **Arguments:**
    - **representations**: `[_Any!]!`
- **_service**: `_Service!`
- **programById**: `ProgramGQLModel` – returns program by its id
  - **Arguments:**
    - **id**: `UUID!`
- **programPage**: `[ProgramGQLModel!]!` – returns programs defined by filter
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `ProgramInputFilter`
- **hello**: `String!`

## Skaláry

#### _Any

#### UUID

#### Date

Date (isoformat)

#### Int

The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

#### String

The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

#### Boolean

The `Boolean` scalar type represents `true` or `false`.

#### DateTime

Date with time (isoformat)

## Vstupní typy

#### SemesterInputFilter

Operators definition on SemesterInputFilter

Input Fields:
- **_or**: `[SemesterInputFilterOr!]` – Filter method
- **_and**: `[SemesterInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### SemesterInputFilterOr

Or operator definition on SemesterInputFilter

Input Fields:
- **_and**: `[SemesterInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### SemesterInputFilterAnd

And operator definition on SemesterInputFilter

Input Fields:
- **_or**: `[SemesterInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### UuidFilter

Integer filter methods, only one constrain allowed

Input Fields:
- **_eq**: `UUID` – operation for select.filter() method
- **_in**: `[UUID!]` – operation for select.filter() method

#### StrFilter

Str filter methods, only one constrain allowed

Input Fields:
- **_eq**: `String` – operation for select.filter() method
- **_le**: `String` – operation for select.filter() method
- **_lt**: `String` – operation for select.filter() method
- **_ge**: `String` – operation for select.filter() method
- **_gt**: `String` – operation for select.filter() method
- **_like**: `String` – operation for select.filter() method
- **_ilike**: `String` – operation for select.filter() method
- **_startswith**: `String` – operation for select.filter() method
- **_endswith**: `String` – operation for select.filter() method

#### LessonInputFilter

Operators definition on LessonInputFilter

Input Fields:
- **_or**: `[LessonInputFilterOr!]` – Filter method
- **_and**: `[LessonInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### LessonInputFilterOr

Or operator definition on LessonInputFilter

Input Fields:
- **_and**: `[LessonInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### LessonInputFilterAnd

And operator definition on LessonInputFilter

Input Fields:
- **_or**: `[LessonInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### TopicInputFilter

Operators definition on TopicInputFilter

Input Fields:
- **_or**: `[TopicInputFilterOr!]` – Filter method
- **_and**: `[TopicInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### TopicInputFilterOr

Or operator definition on TopicInputFilter

Input Fields:
- **_and**: `[TopicInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### TopicInputFilterAnd

And operator definition on TopicInputFilter

Input Fields:
- **_or**: `[TopicInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### StudyPlanLessonInputFilter

Operators definition on StudyPlanLessonInputFilter

Input Fields:
- **_or**: `[StudyPlanLessonInputFilterOr!]` – Filter method
- **_and**: `[StudyPlanLessonInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### StudyPlanLessonInputFilterOr

Or operator definition on StudyPlanLessonInputFilter

Input Fields:
- **_and**: `[StudyPlanLessonInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### StudyPlanLessonInputFilterAnd

And operator definition on StudyPlanLessonInputFilter

Input Fields:
- **_or**: `[StudyPlanLessonInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### ExamInputFilter

Operators definition on ExamInputFilter

Input Fields:
- **_or**: `[ExamInputFilterOr!]` – Filter method
- **_and**: `[ExamInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### ExamInputFilterOr

Or operator definition on ExamInputFilter

Input Fields:
- **_and**: `[ExamInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### ExamInputFilterAnd

And operator definition on ExamInputFilter

Input Fields:
- **_or**: `[ExamInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### EvaluationInputFilter

Operators definition on EvaluationInputFilter

Input Fields:
- **_or**: `[EvaluationInputFilterOr!]` – Filter method
- **_and**: `[EvaluationInputFilterAnd!]` – Filter method
- **student_id**: `UuidFilter` – Filter method
- **examiner_id**: `UuidFilter` – Filter method
- **created**: `DatetimeFilter` – Filter method
- **semester_id**: `UuidFilter` – Filter method
- **attempt**: `IntFilter` – Filter method
- **event_id**: `UuidFilter` – Filter method

#### EvaluationInputFilterOr

Or operator definition on EvaluationInputFilter

Input Fields:
- **_and**: `[EvaluationInputFilterAnd!]` – Filter method
- **student_id**: `UuidFilter` – Filter method
- **examiner_id**: `UuidFilter` – Filter method
- **created**: `DatetimeFilter` – Filter method
- **semester_id**: `UuidFilter` – Filter method
- **attempt**: `IntFilter` – Filter method
- **event_id**: `UuidFilter` – Filter method

#### EvaluationInputFilterAnd

And operator definition on EvaluationInputFilter

Input Fields:
- **_or**: `[EvaluationInputFilterOr!]` – Filter method
- **student_id**: `UuidFilter` – Filter method
- **examiner_id**: `UuidFilter` – Filter method
- **created**: `DatetimeFilter` – Filter method
- **semester_id**: `UuidFilter` – Filter method
- **attempt**: `IntFilter` – Filter method
- **event_id**: `UuidFilter` – Filter method

#### DatetimeFilter

Datetime filter methods, only one constrain allowed

Input Fields:
- **_eq**: `DateTime` – operation for select.filter() method
- **_le**: `DateTime` – operation for select.filter() method
- **_lt**: `DateTime` – operation for select.filter() method
- **_ge**: `DateTime` – operation for select.filter() method
- **_gt**: `DateTime` – operation for select.filter() method

#### IntFilter

Integer filter methods, only one constrain allowed

Input Fields:
- **_eq**: `Int` – operation for select.filter() method
- **_le**: `Int` – operation for select.filter() method
- **_lt**: `Int` – operation for select.filter() method
- **_ge**: `Int` – operation for select.filter() method
- **_gt**: `Int` – operation for select.filter() method
- **_in**: `[Int!]` – operation for select.filter() method

#### StudyPlanInputFilter

Operators definition on StudyPlanInputFilter

Input Fields:
- **_or**: `[StudyPlanInputFilterOr!]` – Filter method
- **_and**: `[StudyPlanInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### StudyPlanInputFilterOr

Or operator definition on StudyPlanInputFilter

Input Fields:
- **_and**: `[StudyPlanInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### StudyPlanInputFilterAnd

And operator definition on StudyPlanInputFilter

Input Fields:
- **_or**: `[StudyPlanInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method

#### StudentInputFilter

Operators definition on StudentInputFilter

Input Fields:
- **_or**: `[StudentInputFilterOr!]` – Filter method
- **_and**: `[StudentInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **user_id**: `UuidFilter` – Filter method
- **program_id**: `UuidFilter` – Filter method

#### StudentInputFilterOr

Or operator definition on StudentInputFilter

Input Fields:
- **_and**: `[StudentInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **user_id**: `UuidFilter` – Filter method
- **program_id**: `UuidFilter` – Filter method

#### StudentInputFilterAnd

And operator definition on StudentInputFilter

Input Fields:
- **_or**: `[StudentInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **user_id**: `UuidFilter` – Filter method
- **program_id**: `UuidFilter` – Filter method

#### SubjectInputFilter

Operators definition on SubjectInputFilter

Input Fields:
- **_or**: `[SubjectInputFilterOr!]` – Filter method
- **_and**: `[SubjectInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### SubjectInputFilterOr

Or operator definition on SubjectInputFilter

Input Fields:
- **_and**: `[SubjectInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### SubjectInputFilterAnd

And operator definition on SubjectInputFilter

Input Fields:
- **_or**: `[SubjectInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### ProgramInputFilter

Operators definition on ProgramInputFilter

Input Fields:
- **_or**: `[ProgramInputFilterOr!]` – Filter method
- **_and**: `[ProgramInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### ProgramInputFilterOr

Or operator definition on ProgramInputFilter

Input Fields:
- **_and**: `[ProgramInputFilterAnd!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

#### ProgramInputFilterAnd

And operator definition on ProgramInputFilter

Input Fields:
- **_or**: `[ProgramInputFilterOr!]` – Filter method
- **id**: `UuidFilter` – Filter method
- **name**: `StrFilter` – Filter method

## Regulérní typy

#### ProgramGQLModel

Program entity, represents an accredited study

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **subjects**: `[SubjectGQLModel!]!` – Program subjects
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `SubjectInputFilter`
- **students**: `[StudentGQLModel!]!` – students
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `StudentInputFilter`
- **guarantorsId**: `UUID` – guarantors of programme
- **guarantors**: `GroupGQLModel` – guarantors of programme
- **licensedId**: `UUID` – Who has got license for programme
- **licensed**: `GroupGQLModel` – Who has got license for programme
- **typeId**: `UUID` – type of programme
- **type**: `ProgramTypeGQLModel` – type of pragramme

#### UserGQLModel

Fields:
- **id**: `UUID!`
- **studies**: `StudentGQLModel` – studies, aka what user is studying (with state)
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `StudentInputFilter`

#### StudentGQLModel

Fields:
- **userId**: `UUID`
- **user**: `UserGQLModel` – who is student
- **programId**: `UUID`
- **program**: `ProgramGQLModel` – which program student is studying
- **stateId**: `UUID`
- **state**: `StateGQLModel` – State of the user study
- **evaluations**: `[EvaluationGQLModel!]!` – given grades
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `EvaluationInputFilter`

#### StateGQLModel

Fields:
- **id**: `UUID!`

#### EvaluationGQLModel

Exam evaluation

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **points**: `Int` – given points for this exam
- **grade**: `String` – given grade / mark
- **attempt**: `Int` – index of attempt
- **passed**: `Boolean` – True if student passed this exam
- **studentId**: `UUID` – id of the student
- **student**: `StudentGQLModel` – student who is examined
- **examinerId**: `UUID` – who examined
- **examiner**: `UserGQLModel` – Who examined
- **semesterId**: `UUID` – to which semester / subject this examination belongs
- **semester**: `SemesterGQLModel` – semester to which this examination belongs to
- **examId**: `UUID` – related exam conditions
- **exam**: `ExamGQLModel` – related exam conditions
- **examEventId**: `UUID`
- **examEvent**: `EventGQLModel`
- **parentId**: `UUID` – id of exam which this is part
- **parent**: `EvaluationGQLModel` – exam of which is this part
- **children**: `[EvaluationGQLModel!]!` – sub parts of this evaluation
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `EvaluationInputFilter`

#### RBACObjectGQLModel

Fields:
- **id**: `UUID!`

#### SemesterGQLModel

Semester entity, allows division of subject into smaller parts

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **order**: `Int` – order in same subject
- **mandatory**: `Boolean` – True if every student must pass this subject
- **credits**: `Int` – credits
- **subjectId**: `UUID` – subject id
- **subject**: `SubjectGQLModel` – subject
- **prerequisites**: `[SubjectGQLModel!]!` – subjects vhcin must be studied at first
- **topics**: `[TopicGQLModel!]!` – Semester topics
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `TopicInputFilter`
- **plans**: `[StudyPlanGQLModel!]!` – plans of study execution
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `StudyPlanInputFilter`

#### SubjectGQLModel

Subject entity

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String!` – subject name
- **nameEn**: `String!` – subject name in english
- **description**: `String!` – subject description
- **descriptionEn**: `String!` – subject description in english
- **programId**: `UUID!` – program id
- **program**: `ProgramGQLModel` – program entity
- **semesters**: `[SemesterGQLModel!]!` – subject semesters
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `SemesterInputFilter`
- **guarantorsId**: `UUID` – guarantors of programme
- **guarantors**: `GroupGQLModel` – guarantors of programme

#### GroupGQLModel

Fields:
- **id**: `UUID!`

#### TopicGQLModel

Topic entity

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – topic name
- **description**: `String` – topic description
- **semesterId**: `UUID` – semester id
- **semester**: `SemesterGQLModel` – semester
- **lessons**: `[LessonGQLModel!]!` – lessons
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `LessonInputFilter`

#### LessonGQLModel

Lesson entity

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **topicId**: `UUID`
- **topic**: `TopicGQLModel`

#### StudyPlanGQLModel

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **semesterId**: `UUID` – ID of Semester to which the plan is related
- **semester**: `SemesterGQLModel` – Semester to which the plan is related
- **lessons**: `[StudyPlanLessonGQLModel!]!` – part of study plan
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `StudyPlanLessonInputFilter`
- **examId**: `UUID` – Exam Rules
- **exam**: `ExamGQLModel` – Exam Rules
- **eventId**: `UUID` – Time period when the plan will live
- **event**: `EventGQLModel` – Time period when the plan will live

#### StudyPlanLessonGQLModel

On row in studyplan

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **order**: `Int` – order in plan
- **length**: `Int` – length in fictive units
- **eventId**: `UUID` – id of event which has been planed for this lesson
- **event**: `EventGQLModel` – event which has been planed for this lesson
- **topicId**: `UUID` – Topic to which the Lesson is related
- **topic**: `TopicGQLModel` – Topic to which the Lesson is related
- **linkedWithId**: `UUID`
- **linkedWith**: `[StudyPlanLessonGQLModel!]!` – list of linked othe planned lessons
- **instructors**: `[UserGQLModel!]!` – whos teach the lesson
- **studyGroups**: `[GroupGQLModel!]!` – study groups
- **facilities**: `[FacilityGQLModel!]!` – places for this lesson

#### EventGQLModel

Fields:
- **id**: `UUID!`

#### FacilityGQLModel

Fields:
- **id**: `UUID!`

#### ExamGQLModel

Exam definition

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String`
- **description**: `String` – extended description of exam conditions
- **minScore**: `Int` – defined minimum points to pass the exam
- **maxScore**: `Int` – defined maximum achievable points
- **parentId**: `UUID` – id of exam which is part
- **parent**: `UUID` – exam is part of exam
- **parts**: `[ExamGQLModel!]!` – exam parts
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `ExamInputFilter`
- **evaluations**: `[EvaluationGQLModel!]!` – evaluations of users during exams
  - **Arguments:**
    - **skip**: `Int`
    - **limit**: `Int`
    - **orderby**: `String`
    - **where**: `EvaluationInputFilter`

#### ProgramTypeGQLModel

Unites attributes into single type

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – name
- **nameEn**: `String` – english name
- **levelTypeId**: `UUID` – level of programme
- **levelType**: `ProgramLevelTypeGQLModel` – level of programme
- **titleTypeId**: `UUID` – level of programme
- **titleType**: `ProgramTitleTypeGQLModel` – level of programme
- **languageTypeId**: `UUID` – level of programme
- **languageType**: `ProgramLanguageTypeGQLModel` – level of programme
- **formTypeId**: `UUID` – level of programme
- **formType**: `ProgramFormTypeGQLModel` – level of programme

#### ProgramLevelTypeGQLModel

determine Bc. / Mgr. / Ph.D.

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – name
- **nameEn**: `String` – english name

#### ProgramTitleTypeGQLModel

Specifies title if ended successfully

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – name
- **nameEn**: `String` – english name

#### ProgramLanguageTypeGQLModel

language definition, often CZ or EN

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – name
- **nameEn**: `String` – english name

#### ProgramFormTypeGQLModel

Fields:
- **id**: `UUID` – primary key
- **lastchange**: `Date` – timestamp
- **created**: `Date` – date & time of unit born
- **createdbyId**: `UUID` – who created this entity
- **changedbyId**: `UUID` – who changed this entity
- **rbacobjectId**: `UUID` – rbac ruling object
- **createdby**: `UserGQLModel` – who created this entity
- **changedby**: `UserGQLModel` – who created this entity
- **rbacobject**: `RBACObjectGQLModel` – rbac holds relations of user
- **name**: `String` – name
- **nameEn**: `String` – english name

#### _Service

Fields:
- **sdl**: `String!`

