import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ClassificationPlanModel(BaseModel):
    __tablename__ = "acclassificationplans"
    
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)

    # Z, KZ, Z+Zk, Zk, ...
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')
    # 
    #     
    # Additional fields or relationships can be defined here.
    # For example:
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')

    description: Mapped[str] = mapped_column(default=None, nullable=True)
    description_en: Mapped[str] = mapped_column(default=None, nullable=True)
    min_score: Mapped[int] = mapped_column(default=None, nullable=True)
    max_score: Mapped[int] = mapped_column(default=None, nullable=True)

    type_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationtypes.id"), default=None, nullable=True, index=True)
    parent_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), default=None, nullable=True, index=True)
