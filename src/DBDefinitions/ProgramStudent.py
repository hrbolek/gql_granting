import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramStudentModel(BaseModel):
    __tablename__ = "acprograms_students"

    user_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("acprograms_studentstates.id"), default=None, nullable=True)
    program_id: Mapped[IDType] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True)
    semester: Mapped[int] = mapped_column(default=None, nullable=True)