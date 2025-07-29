import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ClassificationModel(BaseModel):
    """Holds a particular classification for a student.

    Args:
        id (ID): An primary key.
        order (int): 1 for first attempt.
        classificationlevel_id (ID): e.g., A, B, C, ...
    """
    __tablename__ = "acclassifications"

    path_attribute_name = "path"
    parent_attribute_name = "parent"
    parent_id_attribute_name = "parent_id"
    children_attribute_name = "parts"

    # Materialized path technique
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )

    order: Mapped[int] = mapped_column(default=None, nullable=True, comment="attempt to pass")
    points: Mapped[int] = mapped_column(default=None, nullable=True, comment="points got")
    passed: Mapped[bool] = mapped_column(default=None, nullable=True, comment="passed")

    description: Mapped[str] = mapped_column(default=None, nullable=True, comment="detailed description of exam")

    classificationlevel_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationlevels.id"), index=True, default=None, nullable=True)
    # classificationplan_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), index=True, default=None, nullable=True)
    exam_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), default=None, nullable=True, comment="exam of which is this part")
    semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)
    parent_id: Mapped[IDType] = mapped_column(ForeignKey("acclassifications.id"), index=True, default=None, nullable=True)
    student_id: Mapped[IDType] = mapped_column(ForeignKey("acprograms_students.id"), index=True, default=None, nullable=True)

    # student_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    examiner_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    event_id: Mapped[IDType] = UUIDFKey(ForeignKey("events.id"), default=None, nullable=True)

    semester = relationship(
        "SemesterModel", 
        viewonly=True, 
        uselist=False
    )
    # classificationplan = relationship("ClassificationPlanModel", viewonly=True, uselist=False)
    classificationlevel = relationship(
        "ClassificationLevelModel", 
        viewonly=True, 
        uselist=False
    )
    
    exam = relationship(
        "ClassificationPlanModel", 
        viewonly=True, 
        uselist=False, 
        foreign_keys=[exam_id]
    )

    parent = relationship(
        "ClassificationModel", 
        viewonly=True, 
        remote_side="ClassificationModel.id",
        uselist=False, 
        back_populates="parts",
    )
    # parts = relationship("ClassificationModel", viewonly=True, uselist=True, foreign_keys=[exam_id])
    parts = relationship(
        "ClassificationModel", 
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update"
    )

    student = relationship(
        "ProgramStudentModel", 
        viewonly=True, 
        uselist=False, 
        foreign_keys=[student_id]
    )
    