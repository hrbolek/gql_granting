from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class SubjectModel(BaseModel):
    """Could be a Mathematics.

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        program_id (ID): the program to which subject belongs
    """
    __tablename__ = "acsubjects"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    program_id: Mapped[IDType] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True)
    guarantors_group_id: Mapped[IDType] = UUIDFKey(nullable=True)

    semesters = relationship(
        "SemesterModel", 
        foreign_keys="[SemesterModel.subject_id]",
        uselist=True,
        back_populates="subject",
        cascade="save-update",
        init=True
    )

    program = relationship(
        "ProgramModel",
        foreign_keys="[]"
    )
