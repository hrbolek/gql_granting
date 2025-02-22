import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ClassificationLevelModel(BaseModel):
    """Holds a particular classification level (A, B, C, ...).

    Args:
        id (ID): A primary key.
        name (str): A, B, C, ...
        name_en (str): A, B, C, ...
        ordervalue (int): 1, 2, 3, ...
    """
    __tablename__ = "acclassificationlevels"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    ordervalue: Mapped[int] = mapped_column(default=None, nullable=True)