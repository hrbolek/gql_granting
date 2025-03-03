import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramStudentDocumentModel(BaseModel):
    __tablename__ = "acstudents_documents"

    student_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    document_id: Mapped[IDType] = UUIDFKey(ForeignKey("documents.id"), default=None, nullable=True)
