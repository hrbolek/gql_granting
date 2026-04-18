import datetime
import sqlalchemy
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ProgramStudentModel(BaseModel):
    __tablename__ = "acprograms_students"

    user_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    state_id: Mapped[IDType] = UUIDFKey(ForeignKey("acprograms_studentstates.id"), default=None, nullable=True)
    program_id: Mapped[IDType] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True)
    semester_number: Mapped[int] = mapped_column(default=None, nullable=True)


    @hybrid_property
    def valid(self):
        """Evaluates if the entity is valid based on the current datetime."""
        now = datetime.datetime.now(datetime.timezone.utc)
        if self.startdate and self.enddate:
            return self.startdate <= now <= self.enddate
        elif self.startdate:
            return self.startdate <= now
        elif self.enddate:
            return now <= self.enddate
        return False

    @valid.expression
    def valid(cls):
        return sqlalchemy.and_(
            sqlalchemy.or_(cls.startdate <= func.now(), cls.startdate.is_(None)),
            sqlalchemy.or_(cls.enddate >= func.now(), cls.enddate.is_(None))
        )
    
    program = relationship("ProgramModel", viewonly=True, uselist=False)
    classifications = relationship(
        "ClassificationModel",
        uselist=True,
        viewonly=True
    )