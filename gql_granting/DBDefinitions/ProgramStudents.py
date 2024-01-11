import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class ProgramStudents(BaseModel):
    
    """Represents students enrolled in academic programs.

    Args:
        id (ID): A unique identifier for the student enrollment record.
        program_id (ID): Foreign key referencing the associated program in the 'acprograms' table.
        student_id (ID, optional): Foreign key referencing the associated user (student). Nullable.
        state_id (ID): Foreign key referencing the state of the student enrollment in 'acprograms_studentstates' table.
        semester (int): The academic semester in which the student is enrolled.
        name (str): The name of the student.
        valid (bool): Indicates the validity of the enrollment. Default is True.

    """

    __tablename__ = "acprograms_students"
    id = UUIDColumn()
    
    program_id = Column(ForeignKey("acprograms.id"))
    student_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    state_id = Column(ForeignKey("acprograms_studentstates.id"), index=True)
    semester = Column(Integer)
    name = Column(String)
    valid = Column(Boolean, default=lambda item: True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
