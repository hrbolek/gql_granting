from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class TopicModel(BaseModel):
    """Aka Functions"""
    __tablename__ = "actopics"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    order: Mapped[int] = mapped_column(default=None, nullable=True)
    semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)

    semester = relationship(
        "SemesterModel",
        back_populates="topics",
        init=True,
        uselist=False,
    )

    lessons = relationship(
        "LessonModel",
        
        uselist=True,
        back_populates="topic",
        cascade="save-update",
        init=True
    )