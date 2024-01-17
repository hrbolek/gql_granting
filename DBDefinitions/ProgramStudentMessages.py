import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey


class ProgramStudentMessages(BaseModel):
    """Represents messages related to student programs.

    Args:
        id (ID): A unique identifier for the message.
        name (str): The name of the message.
        description (str): Additional details or description of the message.
        student_id (ID): Foreign key referencing the associated student in the 'acprograms_students' table.
        program_id (ID): Foreign key referencing the associated program in the 'acprograms' table.
        date (DateTime): The date and time when the message was created.

    
    """
    __tablename__ = "acprograms_studentmessages"
    id = UUIDColumn()
    name = Column(String)
    description = Column(String)
    student_id = Column(ForeignKey("acprograms_students.id"), index=True)
    program_id = Column(ForeignKey("acprograms.id"), index=True)
    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
