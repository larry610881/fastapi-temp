from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class WebsocketsStatisticsEntry(Base):
    __tablename__ = "websockets_statistics_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    app_id: Mapped[str] = mapped_column(String(255))
    peak_connection_count: Mapped[int] = mapped_column(Integer)
    websocket_message_count: Mapped[int] = mapped_column(Integer)
    api_message_count: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
