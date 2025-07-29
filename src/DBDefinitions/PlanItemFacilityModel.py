from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class PlanItemFacilityModel(BaseModel):
    """Where should teach"""
    __tablename__ = "acplanitemfacilities"

    planitem_id: Mapped[IDType] = mapped_column(ForeignKey("plan_lessons.id"), index=True, default=None, nullable=True)
    facility_id: Mapped[IDType] = UUIDFKey(ForeignKey("facilities.id"), index=True, default=None, nullable=True)
    
    planitem = relationship(
        "PlanItemModel",
        uselist=False,
        viewonly=True
    )