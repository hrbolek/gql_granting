from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester"""
    __tablename__ = "acsemesters"

    order: Mapped[int] = mapped_column(default=None, nullable=True)
    credits: Mapped[int] = mapped_column(default=None, nullable=True)
    subject_id: Mapped[IDType] = mapped_column(ForeignKey("acsubjects.id"), index=True, default=None, nullable=True)
    classificationtype_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationtypes.id"), index=True, default=None, nullable=True)
