from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        type_id (ID): structure defining the kind of program
    """
    __tablename__ = "acprograms"
    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="name of the program")
    name_en: Mapped[str] = mapped_column(default=None, nullable=True, comment="english name of the program")
    type_id: Mapped[IDType] = mapped_column(ForeignKey("acprogramtypes.id"), index=True, default=None, nullable=True)
    group_id: Mapped[IDType] = UUIDFKey(ForeignKey("groups.id"), default=None, nullable=True) # garanti programu
    licenced_group_id: Mapped[IDType] = UUIDFKey(ForeignKey("groups.id"), default=None, nullable=True) # fakulta nebo skola

