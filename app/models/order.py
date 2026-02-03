from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(28), primary_key=True, index=True)
    rno: Mapped[str] = mapped_column(String(6))
    storeId: Mapped[str] = mapped_column(String(6), index=True)
    
    # 金額欄位 (對應 Laravel unsignedInteger)
    before_discount_tx_price: Mapped[int] = mapped_column(Integer, default=0)
    tx_discount_amount: Mapped[int] = mapped_column(Integer, default=0)
    after_discount_tx_price: Mapped[int] = mapped_column(Integer, default=0)
    
    before_discount_ex_price: Mapped[int] = mapped_column(Integer, default=0)
    ex_discount_amount: Mapped[int] = mapped_column(Integer, default=0)
    after_discount_ex_price: Mapped[int] = mapped_column(Integer, default=0)
    
    payable_amount: Mapped[int] = mapped_column(Integer, default=0)
    amount_actually_paid: Mapped[int] = mapped_column(Integer, default=0)
    
    pay_type: Mapped[str] = mapped_column(String(15))
    
    # 時間戳 (Laravel timestamps & softDeletes)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
