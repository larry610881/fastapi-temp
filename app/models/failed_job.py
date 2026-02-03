from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class FailedJob(Base):
    __tablename__ = "failed_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(255), unique=True)
    connection: Mapped[str] = mapped_column(Text)
    queue: Mapped[str] = mapped_column(Text)
    payload: Mapped[str] = mapped_column(Text) # LongText in migration, Text in SQLAlchemy usually sufficient or use dialect specific
    exception: Mapped[str] = mapped_column(Text) # LongText
    failed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
