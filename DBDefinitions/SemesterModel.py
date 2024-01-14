import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey
from sqlalchemy.orm import relationship

class SemesterModel(BaseModel):
    
    """ Represents an academic semester.

    Args:
        id (ID): A unique identifier for the semester.
        order (int): The order or number of the semester.
        credits (int): The number of credits associated with the semester.
        subject_id (ID): Foreign key referencing the associated subject in the 'acsubjects' table.
        classificationtype_id (ID): Foreign key referencing the classification type in the 'acclassificationtypes' table.
"""

    __tablename__ = "acsemesters"
    id = UUIDColumn()
    order = Column(Integer)
    credits = Column(Integer)
    subject_id = Column(ForeignKey("acsubjects.id"), index=True)
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # classification_type = relationship("ClassificationTypeModel", back_populates="semester", uselist=False)
    # subject = relationship('SubjectModel', back_populates='semesters')
    # classifications = relationship('ClassificationModel', back_populates='classificationsemesters', uselist = True)
    # themes = relationship('StudyThemesModel', back_populates='studysemesters')


##############################################
