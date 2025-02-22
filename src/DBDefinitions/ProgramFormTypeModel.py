from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramFormTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Presenční
        name_en (str): aka Present
    """
    __tablename__ = "acprogramforms"
    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="name of the program")
    name_en: Mapped[str] = mapped_column(default=None, nullable=True, comment="english name of the program")
