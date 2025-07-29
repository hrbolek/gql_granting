import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, IDType, UUIDFKey


class AdmissionModel(BaseModel):
    __tablename__ = "admissions"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the admission entry")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the admission entry")

    state_id: Mapped[IDType] = UUIDFKey(nullable=True, comment="stav přijímacího řízení")
    program_id: Mapped[IDType] = UUIDFKey(nullable=True, comment="Program, pro který je přijímací řízení vypsáno")
    payment_info_id: Mapped[IDType] = mapped_column(ForeignKey("admission_payment_infos.id"), nullable=True, default=None, comment="platební podmínky")

    application_start_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Od kdy lze podávat přihlášky")
    application_last_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Poslední možnost podání přihlášky")
    end_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Konec přijímacího řízení")
    condition_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Do kdy lze doložit splnění podmínek")
    payment_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Do kdy lze zaplatit poplatek")
    condition_extended_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Prodloužená lhůta pro doložení splnění podmínek")
    request_condition_extend_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Lhůta do kdy lze požádat o prodloužení pro doložení splnění podmínek")
    request_extra_conditions_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Lhůta do kdy lze požádat o specifické podmínky přijímacího řízení")
    request_extra_date_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Lhůta do kdy lze požádat o extra termín přijímacích zkoušek")
    exam_start_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="První možný den přijímacích zkoušek")
    exam_last_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Poslední možný den přijímacích zkoušek")
    student_entry_date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Den zápisu")

    # discipline = relationship("PaymentInfoModel", viewonly=True, uselist=False, lazy="joined") # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
    payment_info = relationship("PaymentInfoModel", viewonly=True, uselist=False, lazy="joined") # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html

    pass