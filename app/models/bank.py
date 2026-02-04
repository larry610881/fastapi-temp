from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Bank(Base):
    __tablename__ = "banks"

    bank_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    payment_institution_code: Mapped[str] = mapped_column(String(10), comment="支付機構代碼")
    bank_code: Mapped[str] = mapped_column(String(7), unique=True, comment="銀行代碼")
    bank_name: Mapped[str] = mapped_column(String(50), comment="銀行名稱")
    bank_short_name: Mapped[str] = mapped_column(String(20), comment="銀行簡稱")
    bank_type: Mapped[str] = mapped_column(String(10), comment="是否為併機行 (Y:併機行/N:非併機行)")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="狀態 (1:啟用/0:停用)")
    effective_date: Mapped[datetime] = mapped_column(Date, comment="生效日期")
    expire_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True, comment="失效日期")
    create_user: Mapped[str] = mapped_column(String(20), default="SYSTEM", comment="建立人員")
    update_user: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="更新人員")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
