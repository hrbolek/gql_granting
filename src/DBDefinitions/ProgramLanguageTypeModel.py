from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramLanguageTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Čeština
        name_en (str): aka Czech
    """
    __tablename__ = "acprogramlanguages"
    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="name of the program")
    name_en: Mapped[str] = mapped_column(default=None, nullable=True, comment="english name of the program")
