import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ClassificationTypeModel(BaseModel):
    __tablename__ = "acclassificationtypes"
    
    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)

    # Z, KZ, Z+Zk, Zk, ...
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')
    # 
    #     
    # Additional fields or relationships can be defined here.
    # For example:
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')
