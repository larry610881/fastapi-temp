from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.dialects.mysql import INTEGER as UnsignedInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(28), primary_key=True, comment="訂單編號")
    rno: Mapped[str] = mapped_column(String(6), comment="流水號 000001~999999")
    storeId: Mapped[str] = mapped_column(String(6), index=True, comment="商店編號")
    
    # Prices - Unsigned Integers
    before_discount_tx_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="應稅商品折扣前價錢")
    tx_discount_amount: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="應稅商品折扣額")
    after_discount_tx_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="應稅商品折扣後額")
    before_discount_ex_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="免稅商品折扣前價錢")
    ex_discount_amount: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="免稅商品折扣額")
    after_discount_ex_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="免稅商品折扣後額")
    payable_amount: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="訂單應付金額")
    amount_actually_paid: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), comment="訂單實付金額")
    
    pay_type: Mapped[str] = mapped_column(String(15), comment="付款方式")
    phone: Mapped[Optional[str]] = mapped_column(String(255), default="NO Phone", nullable=True, comment="Phone (Encrypted)")
    op_gid: Mapped[Optional[str]] = mapped_column(String(50), default="", nullable=True, comment="Open Point Member GID")
    
    # No Discount Fields
    no_discount_total_price: Mapped[int] = mapped_column(Integer, default=0, comment="No Discount Total Price")
    tx_no_discount_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), default=0, comment="TX No Discount Price")
    ex_no_discount_price: Mapped[int] = mapped_column(UnsignedInteger(unsigned=True), default=0, comment="EX No Discount Price")

    # API / SDK Fields
    SDK_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    TRI_Api_Request: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # ITRI Fields
    ITRI_Order_No: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="中研院傳進來的訂單編號")
    ITRI_rno: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="中研院傳進來的rno")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")
