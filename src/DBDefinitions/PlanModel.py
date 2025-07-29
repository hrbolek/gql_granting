from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanModel(BaseModel):
    """Aka Functions"""
    __tablename__ = "plans"

    semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)
    exam_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), index=True, default=None, nullable=True)
    event_id: Mapped[IDType] = UUIDFKey(ForeignKey("events.id"), index=True, default=None, nullable=True)

    semester = relationship(
        "SemesterModel",
        back_populates="plans",
        uselist=False,
        viewonly=True, 
    )

    exam = relationship(
        "ClassificationPlanModel",
        back_populates="plan",
        uselist=False,
        init=True,
        cascade="save-update"
    )

    planitems = relationship(
        "PlanItemModel",
        back_populates="plan",
        uselist=True,
        init=True,
        cascade="save-update"
    )