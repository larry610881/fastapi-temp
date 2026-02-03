from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Store(Base):
    __tablename__ = "stores"

    storeId: Mapped[str] = mapped_column(String(6), primary_key=True, index=True)
    type: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(String(20)) # 原 migration 未指定長度，給預設
    qr_code: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # 來自 2023_10_12_160153 擴充
    gps: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # 來自 2023_08_31_105248 擴充
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
