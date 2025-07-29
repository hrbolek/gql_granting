from sqlalchemy import (
    Column, 
    String, 
    DateTime, 
    Float,
    ForeignKey
)

from .BaseModel import BaseModel, UUIDFKey

from sqlalchemy.orm import Mapped, mapped_column

class PaymentInfoModel(BaseModel):
    __tablename__ = "admission_payment_infos"

    account_number: Mapped[str] = mapped_column(nullable=True, default=None, comment="číslo účtu s kódem banky za lomítkem")
    specific_symbol: Mapped[str] = mapped_column(nullable=True, default=None, comment="specifický symbol")
    constant_symbol: Mapped[str] = mapped_column(nullable=True, default=None, comment="konstantní symbol")
    IBAN: Mapped[str] = mapped_column(nullable=True, default=None, comment="IBAN code")
    SWIFT: Mapped[str] = mapped_column(nullable=True, default=None, comment="SWIFT bank code")
    amount: Mapped[float] = mapped_column(nullable=True, default=None, comment="Částka k zaplacení")