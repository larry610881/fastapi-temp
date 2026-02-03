from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Boolean, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    account: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60))
    department: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    owner_name: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    logintimes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
