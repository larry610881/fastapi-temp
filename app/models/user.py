from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, comment="Primary Key")
    account: Mapped[str] = mapped_column(String(20), unique=True, comment="User Account")
    password: Mapped[str] = mapped_column(String(255), comment="Encrypted Password")
    department: Mapped[Optional[str]] = mapped_column(String(20), comment="Department", nullable=True)
    owner_name: Mapped[Optional[str]] = mapped_column(String(10), comment="Owner Name", nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Expiry Date")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Is Disabled")
    logintimes: Mapped[Optional[int]] = mapped_column(Integer, comment="Login Times", nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
