from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, IDType, UUIDFKey



class PaymentModel(BaseModel):
    __tablename__ = "admission_payments"

    payment_info_id: Mapped[IDType] = mapped_column(ForeignKey("admission_payment_infos.id"), nullable=True, default=None, comment="Generální platební podmínky")
    bank_unique_data: Mapped[str] = mapped_column(nullable=True, default=None, comment="unikátní identifikátor platby vystavený bankou (link do banky)")
    variable_symbol: Mapped[str] = mapped_column(nullable=True, default=None, comment="uvedený variabilní symbol")
    student_id: Mapped[IDType] = UUIDFKey(comment="identifikovaná přihláška / student")
    amount: Mapped[float] = mapped_column(nullable=True, default=None, comment="zaplacená částka")

    pass