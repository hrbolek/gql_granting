from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanModel(BaseModel):
    """Aka Functions"""
    __tablename__ = "acplans"

    semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)
    classificationplan_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), index=True, default=None, nullable=True)