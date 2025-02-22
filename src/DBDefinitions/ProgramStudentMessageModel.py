import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramStudentMessageModel(BaseModel):
    __tablename__ = "acprograms_studentmessages"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    student_id: Mapped[IDType] = UUIDFKey(nullable=True)
    program_id: Mapped[IDType] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), default=None, nullable=True)