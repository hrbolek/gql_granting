from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanItemGroupModel(BaseModel):
    """Whos being teach"""
    __tablename__ = "acplanitemgroups"

    planitem_id: Mapped[IDType] = mapped_column(ForeignKey("plan_lessons.id"), index=True, default=None, nullable=True)
    group_id: Mapped[IDType] = UUIDFKey(ForeignKey("groups.id"), index=True, default=None, nullable=True)
    
    planitem = relationship(
        "PlanItemModel",
        uselist=False,
        viewonly=True
    )