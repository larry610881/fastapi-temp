from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[str] = mapped_column(String(28), ForeignKey('orders.id'), primary_key=True, comment="訂單編號")
    plu_code: Mapped[str] = mapped_column(String(20), primary_key=True, comment="商品PluCode")
    name: Mapped[str] = mapped_column(String(255), comment="商品名稱")
    price: Mapped[int] = mapped_column(Integer, comment="商品價錢")
    count: Mapped[int] = mapped_column(Integer, comment="商品購買數量")
    tax_flg: Mapped[int] = mapped_column(TINYINT, comment="商品稅別(00 => 應稅(已含稅)、 01 => 免稅)")
    is_discount: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否要打折")
    discount_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="打折類型(0 => 百分比、1 => 金額)")
    discount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="折扣率或金額")
    discount_fra_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="小數點處理方式(0 => 無條件進位　1 => 四捨五入　2 => 無條件捨去)")
    no_discount_type: Mapped[int] = mapped_column(Integer, default=0, comment="No Discount Type")
    cherish_flg: Mapped[int] = mapped_column(TINYINT, default=0, comment="珍食標記 (0: 否, 1: 是)")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")

    # Composite primary key is handled by primary_key=True on columns, 
    # but explicit constraint can be added if needed, though declarative handles it.
