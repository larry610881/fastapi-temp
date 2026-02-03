from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(28), ForeignKey('orders.id'), index=True)
    status: Mapped[int] = mapped_column(Integer, default=0, comment="0 => 尚未付款; 1 => 付款完成; 2 => 已退貨")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="附屬訊息")
    operator: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default=None)
    
    # Timestamps (Manually defined in legacy as only created_at, but we add softDeletes too)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="狀態產生時間")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")
