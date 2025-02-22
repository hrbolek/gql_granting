from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType


class ProgramTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        form_id (ID): defines a form (distant, present)
        language_id (ID): defines a language (Czech, English)
        level_id (ID): defines a level (Bachelor, Master, Doctoral, ... )
        title_id (ID): defines a title (Bc., MSc., Ph.D., ...)
    """
    __tablename__ = "acprogramtypes"

    name: Mapped[str] = mapped_column(default=None, nullable=True, comment="name of the program type")
    name_en: Mapped[str] = mapped_column(default=None, nullable=True, comment="english name of the program type")
    form_id: Mapped[IDType] = mapped_column(ForeignKey("acprogramforms.id"), index=True, default=None, nullable=True)
    language_id: Mapped[IDType] = mapped_column(ForeignKey("acprogramlanguages.id"), index=True, default=None, nullable=True)
    level_id: Mapped[IDType] = mapped_column(ForeignKey("acprogramlevels.id"), index=True, default=None, nullable=True)
    title_id: Mapped[IDType] = mapped_column(ForeignKey("acprogramtitles.id"), index=True, default=None, nullable=True)
