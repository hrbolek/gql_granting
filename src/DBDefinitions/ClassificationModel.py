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

    order: Mapped[int] = mapped_column(default=None, nullable=True, comment="attempt to pass")
    points: Mapped[int] = mapped_column(default=None, nullable=True, comment="points got")
    passed: Mapped[bool] = mapped_column(default=None, nullable=True, comment="passed")

    description: Mapped[str] = mapped_column(default=None, nullable=True, comment="detailed description of exam")

    classificationlevel_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationlevels.id"), index=True, default=None, nullable=True)
    # classificationplan_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), index=True, default=None, nullable=True)
    exam_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), default=None, nullable=True, comment="exam of which is this part")
    semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)
    parent_id: Mapped[IDType] = mapped_column(ForeignKey("acclassifications.id"), index=True, default=None, nullable=True)

    student_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    examiner_id: Mapped[IDType] = UUIDFKey(ForeignKey("users.id"), default=None, nullable=True)
    event_id: Mapped[IDType] = UUIDFKey(ForeignKey("events.id"), default=None, nullable=True)

    semester = relationship("SemesterModel", viewonly=True, uselist=False)
    # classificationplan = relationship("ClassificationPlanModel", viewonly=True, uselist=False)
    classificationlevel = relationship("ClassificationLevelModel", viewonly=True, uselist=False)
    exam = relationship("ClassificationPlanModel", viewonly=True, uselist=False, foreign_keys=[exam_id])
    parent = relationship("ClassificationModel", viewonly=True, uselist=False, foreign_keys=[parent_id])
    # parts = relationship("ClassificationModel", viewonly=True, uselist=True, foreign_keys=[exam_id])
    parts = relationship("ClassificationModel", viewonly=True, uselist=True, primaryjoin="ClassificationModel.parent_id==ClassificationModel.id")
    # student = relationship("ProgramStudenModel", viewonly=True, uselist=False, foreign_keys=[student_id])
    