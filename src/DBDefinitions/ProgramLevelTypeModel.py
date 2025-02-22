from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramLevelTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Bakalář
        name_en (str): aka Bachelor
        length (int): length of study
        priority (int): allows to compare two programs and derive appropriate order
    """
    __tablename__ = "acprogramlevels"

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)
    length: Mapped[int] = mapped_column(default=None, nullable=True, comment="standard length of study")
    priority: Mapped[int] = mapped_column(default=None, nullable=True, comment="1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.")