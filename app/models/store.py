from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    storeId: Mapped[str] = mapped_column(String(6), unique=True, index=True)
    type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True) # Match DB VARCHAR(20)
    QRcode: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Match DB state (likely nullable)
    gps_limitLat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    gps_limitLng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
