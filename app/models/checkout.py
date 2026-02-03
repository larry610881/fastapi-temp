from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class CheckoutSmsConsolidateFile(Base):
    __tablename__ = "checkout_sms_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    op_gid: Mapped[Optional[str]] = mapped_column(String(50), comment="GID")
    session_start: Mapped[str] = mapped_column(String(255), comment="session_start") # String default 255
    order_id: Mapped[Optional[str]] = mapped_column(String(28), comment="訂單編號")
    type: Mapped[str] = mapped_column(String(255), comment="調解類型")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CheckoutSmsDetailFile(Base):
    __tablename__ = "checkout_sms_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    op_gid: Mapped[Optional[str]] = mapped_column(String(50), comment="GID")
    session_start: Mapped[str] = mapped_column(String(255), comment="session_start")
    order_id: Mapped[Optional[str]] = mapped_column(String(28), comment="訂單編號")
    type: Mapped[str] = mapped_column(String(255), comment="調解類型")
    plu_code: Mapped[str] = mapped_column(Text, comment="PLU Code(8||13)")
    count: Mapped[int] = mapped_column(Integer, comment="購買數量") # unsignedSmallInteger -> Integer
    name: Mapped[str] = mapped_column(String(50), comment="商品名稱")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CheckoutPayuniCredithash(Base):
    __tablename__ = "checkout_payuni_credithash"

    gid: Mapped[str] = mapped_column(String(255), primary_key=True)
    credithash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
