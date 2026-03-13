import strawberry

from .StudentGQLModel import StudentGQLModel, StudentInputFilter, StudentQuery as _StudentQuery, StudentMutation as _StudentMutation
from .StudentDocumentGQLModel import StudentDocumentQuery, StudentDocumentMutation



@strawberry.interface(name="StudentAllQuery")
class StudentQuery(
    _StudentQuery,
    StudentDocumentQuery
):
    pass

@strawberry.interface(name="StudentAllMutation")
class StudentMutation(
    _StudentMutation,
    StudentDocumentMutation
):
    pass
