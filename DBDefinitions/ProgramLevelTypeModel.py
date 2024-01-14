import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class ProgramLevelTypeModel(BaseModel):
    """Holds a particular level type.

    Args:
        id (ID): An primary key.
        name (str): aka Bakalář
        name_en (str): aka Bachelor
        length (ID): length of study
        priority (ID): allows to compare two programs and derive appropriate order
    """
    __tablename__ = "acprogramlevels"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    length = Column(Integer)
    priority = Column(Integer)  # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.
    # bachelor, magister, doctoral

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
