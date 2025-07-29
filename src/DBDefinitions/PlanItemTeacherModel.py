from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanItemTeacherModel(BaseModel):
    """Who should teach"""
    __tablename__ = "acplanitemteachers"

    planitem_id: Mapped[IDType] = mapped_column(ForeignKey("plan_lessons.id"), index=True, default=None, nullable=True)
    user_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), index=True, default=None, nullable=True)
    
    planitem = relationship(
        "PlanItemModel",
        uselist=False,
        viewonly=True
    )