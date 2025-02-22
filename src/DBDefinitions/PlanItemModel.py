from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanItemModel(BaseModel):
    """Aka item in study plan"""
    __tablename__ = "acplanitems"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    length: Mapped[int] = mapped_column(default=None, nullable=True, comment="amount of virtual units")

    plan_id: Mapped[IDType] = mapped_column(ForeignKey("aclessontypes.id"), index=True, default=None, nullable=True)
    lessontype_id: Mapped[IDType] = mapped_column(ForeignKey("acplans.id"), index=True, default=None, nullable=True)
    topic_id: Mapped[IDType] = mapped_column(ForeignKey("actopics.id"), index=True, default=None, nullable=True)
    linked_with_id: Mapped[IDType] = mapped_column(ForeignKey("acplanitems.id"), index=True, default=None, nullable=True)
    event_id: Mapped[IDType] = UUIDFKey(ForeignKey("events.id"), index=True, default=None, nullable=True)

    teachers = relationship("PlanItemTeacherModel")
    groups = relationship("PlanItemGroupModel")
    facilities = relationship("PlanItemFacilityModel")