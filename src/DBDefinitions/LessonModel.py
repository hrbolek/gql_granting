from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class LessonModel(BaseModel):
    """Lecture, 2h."""
    __tablename__ = "aclessons"

    topic_id: Mapped[IDType] = mapped_column(ForeignKey("actopics.id"), index=True, default=None, nullable=True)
    type_id: Mapped[IDType] = mapped_column(ForeignKey("aclessontypes.id"), index=True, default=None, nullable=True)
    count: Mapped[int] = mapped_column(default=None, nullable=True)