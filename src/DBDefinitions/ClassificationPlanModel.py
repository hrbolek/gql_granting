import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

class ClassificationPlanModel(BaseModel):
    __tablename__ = "acclassificationplans"
    
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

    name: Mapped[str] = mapped_column(default=None, nullable=True)
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)

    description: Mapped[str] = mapped_column(default=None, nullable=True)
    description_en: Mapped[str] = mapped_column(default=None, nullable=True)
    min_score: Mapped[int] = mapped_column(default=None, nullable=True)
    max_score: Mapped[int] = mapped_column(default=None, nullable=True)

    type_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationtypes.id"), default=None, nullable=True, index=True)
    parent_id: Mapped[IDType] = mapped_column(ForeignKey("acclassificationplans.id"), default=None, nullable=True, index=True)
    # plan_id: Mapped[IDType] = mapped_column(ForeignKey("plans.id"), default=None, nullable=True, index=True)

    # semester_id: Mapped[IDType] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True)

    parent = relationship(
        "ClassificationPlanModel",
        viewonly=True, 
        remote_side="ClassificationPlanModel.id",
        uselist=False,
        back_populates="parts",
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    parts = relationship(
        "ClassificationPlanModel", 
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    evaluations = relationship(
        "ClassificationModel", 
        back_populates="exam",
        uselist=True,
        init=True,
        cascade="save-update"
    ) # https://docs.sqlalchemy.org/en/20/orm/self_referential.html

    plan = relationship(
        "PlanModel",
        uselist=False,
        viewonly=True
    )


