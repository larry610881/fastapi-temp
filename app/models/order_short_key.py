from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class OrderShortKey(Base):
    __tablename__ = "order_short_keys"

    short_key: Mapped[str] = mapped_column(String(6), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(28))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
