from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Gps(Base):
    __tablename__ = "gps"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    check_gps: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否檢查 GPS 定位")
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
