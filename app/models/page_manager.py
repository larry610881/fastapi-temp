from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class PageManager(Base):
    __tablename__ = "page_managers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True) # Added in later migration
    name: Mapped[str] = mapped_column(String(20))
    subject: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
