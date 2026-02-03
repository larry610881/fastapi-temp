from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Text, DateTime, Integer, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class SendToSCHostData(Base):
    __tablename__ = "send_to_s_c_host_data"

    id: Mapped[str] = mapped_column(String(28), primary_key=True) # Logic: Date + 6 digit store + 14 digit seq. Match DB logic.
    storeId: Mapped[str] = mapped_column(String(6))
    data: Mapped[dict] = mapped_column(JSON)
    
    # Original migration has foreign key to orders.id
    # $table->foreign('id')->on('orders')->references('id');
    # Note: SQLAlchemy might need explicit ForeignKey define if we want it to manage constraints, 
    # but for receiving existing DB, matching column type is key.
    # We can add ForeignKey('orders.id') if strictly enforcing.
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # "is_cancel" added in 2024_02_23
    is_cancel: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0) 


class SendToSCHostDailyData(Base):
    __tablename__ = "send_to_s_c_host_daily_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    data: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
