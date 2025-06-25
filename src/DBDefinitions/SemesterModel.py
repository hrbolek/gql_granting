from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester"""
    __tablename__ = "acsemesters"

    order: Mapped[int] = mapped_column(default=None, nullable=True)
    credits: Mapped[int] = mapped_column(default=None, nullable=True)
    subject_id: Mapped[IDType] = mapped_column(ForeignKey("acsubjects.id"), index=True, default=None, nullable=True)
    classificationtype_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationtypes.id"), index=True, default=None, nullable=True)

    subject = relationship(
        "SubjectModel",
        back_populates="semesters",
        init=True,
        uselist=False,
    )

    topics = relationship(
        "TopicModel",
        foreign_keys="[TopicModel.semester_id]",
        uselist=True,
        back_populates="semester",
        cascade="save-update",
        init=True
    )