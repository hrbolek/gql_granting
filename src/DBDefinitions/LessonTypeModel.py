import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class LessonTypeModel(BaseModel):
    __tablename__ = "aclessontypes"
    # lectures, excersise, laboratory, ...

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    abbr: Mapped[str] = mapped_column(default=None, nullable=True)