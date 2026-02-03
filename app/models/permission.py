from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(125))
    guard_name: Mapped[str] = mapped_column(String(125))
    
    # 來自 2021_12_08 擴充
    subject: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sort: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("name", "guard_name", name="uq_permission_name_guard"),)

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(125))
    guard_name: Mapped[str] = mapped_column(String(125))
    subject: Mapped[str] = mapped_column(String(50), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("name", "guard_name", name="uq_role_name_guard"),)
