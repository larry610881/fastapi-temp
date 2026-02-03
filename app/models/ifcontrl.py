from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class IfContrl(Base):
    __tablename__ = "ifcontrls"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gm_id: Mapped[str] = mapped_column(Text)
    storeId: Mapped[str] = mapped_column(String(6), index=True)
    short_name: Mapped[str] = mapped_column(Text)
    long_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # 來自 2024_11_15 擴充
    corp_name: Mapped[str] = mapped_column(Text)
    corp_name_2: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    corp_id: Mapped[str] = mapped_column(Text)
    
    dis_flg: Mapped[str] = mapped_column(Text)
    dis_type: Mapped[str] = mapped_column(Text)
    discount: Mapped[str] = mapped_column(Text)
    dis_fra_flg: Mapped[str] = mapped_column(Text)
    ex_dis_flg: Mapped[str] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
