from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Boolean, Table, Column, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

# Association Tables
model_has_roles = Table(
    'model_has_roles',
    Base.metadata,
    Column('role_id', String(36), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('model_type', String(255), primary_key=True),
    Column('model_id', String(36), primary_key=True),
)

model_has_permissions = Table(
    'model_has_permissions',
    Base.metadata,
    Column('permission_id', String(36), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
    Column('model_type', String(255), primary_key=True),
    Column('model_id', String(36), primary_key=True),
)

role_has_permissions = Table(
    'role_has_permissions',
    Base.metadata,
    Column('permission_id', String(36), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', String(36), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
)

class Permission(Base):
    __tablename__ = "permissions"
    
    # Standard Spatie columns, migrated to UUID in legacy
    id: Mapped[str] = mapped_column(String(36), primary_key=True) 
    name: Mapped[str] = mapped_column(String(125)) # Migration comment suggests 125, but usually string default 255. Will verify.
    guard_name: Mapped[str] = mapped_column(String(125))
    
    # Custom added columns
    subject: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    pid: Mapped[Optional[str]] = mapped_column(String(36), nullable=True) # UUID
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # TinyInteger in legacy

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(125))
    guard_name: Mapped[str] = mapped_column(String(125))
    
    # Custom added columns
    subject: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    storeId: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Relationships (Optional, but good for understanding)
    # permissions: Mapped[List["Permission"]] = relationship(secondary=role_has_permissions)
