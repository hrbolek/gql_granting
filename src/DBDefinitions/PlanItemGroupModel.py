from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanItemGroupModel(BaseModel):
    """Whos being teach"""
    __tablename__ = "acplanitemgroups"

    planitem_id: Mapped[IDType] = mapped_column(ForeignKey("acplanitems.id"), index=True, default=None, nullable=True)
    group_id: Mapped[IDType] = UUIDFKey(ForeignKey("groups.id"), index=True, default=None, nullable=True)
    