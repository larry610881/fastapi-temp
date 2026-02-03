from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    # 複合主鍵 (Composite Primary Key)
    id: Mapped[str] = mapped_column(String(28), ForeignKey("orders.id"), primary_key=True)
    plu_code: Mapped[str] = mapped_column(String(13), primary_key=True)
    
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    tax_flg: Mapped[str] = mapped_column(String(2)) # 00: 應稅, 01: 免稅
    
    is_discount: Mapped[bool] = mapped_column(Boolean, default=False)
    discount_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 0: %, 1: $
    discount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    discount_fra_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 0: 進位, 1: 四捨五入, 2: 捨去
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
