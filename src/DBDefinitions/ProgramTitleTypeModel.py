from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramTitleTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Bc.
        name_en (str): aka Bc.
    """
    __tablename__ = "acprogramtitles"

    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="e.g., Bc., Mgr., Ing, etc.")
    name_en: Mapped[str] = mapped_column(default=None, nullable=True, comment="english equivalent")
