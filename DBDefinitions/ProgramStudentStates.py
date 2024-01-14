import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class ProgramStudentStates(BaseModel):
    """Represents different states of student enrollment in academic programs.

    Args:
        id (ID): A unique identifier for the student state.
        name (str): The name of the student state.
        name_en (str): The English name of the student state.
        
    """
    __tablename__ = "acprograms_studentstates"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    
