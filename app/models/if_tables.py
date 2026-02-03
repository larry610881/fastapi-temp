from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class IfContrl(Base):
    __tablename__ = "ifcontrls"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True, comment="Primary Key")
    gm_id: Mapped[str] = mapped_column(Text, comment="業務ID(2)")
    storeId: Mapped[str] = mapped_column(String(6), comment="門市Code(6)", index=True)
    short_name: Mapped[str] = mapped_column(Text, comment="門市名稱（略式）(6)")
    corp_name: Mapped[str] = mapped_column(Text, comment="統一發票公司名１(24)")
    corp_name_2: Mapped[Optional[str]] = mapped_column(Text, comment="統一發票公司名２(24)")
    corp_id: Mapped[str] = mapped_column(Text, comment="統一發票公司代號(8)")
    dis_flg: Mapped[str] = mapped_column(Text, comment="折扣Key區分(1)")
    dis_type: Mapped[str] = mapped_column(Text, comment="折扣區分(1)")
    discount: Mapped[str] = mapped_column(Text, comment="折扣率/金額(4)")
    dis_fra_flg: Mapped[str] = mapped_column(Text, comment="折扣端數處理區分(1)")
    ex_dis_flg: Mapped[str] = mapped_column(Text, comment="免税商品折扣區分(1)")
    long_name: Mapped[Optional[str]] = mapped_column(Text, comment="Long Name", nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")


class IfPluExt(Base):
    __tablename__ = "ifpluexts"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gmid: Mapped[str] = mapped_column(Text, comment="業務ID(5T,2)")
    mkbn: Mapped[str] = mapped_column(Text, comment="Maintenance區分(1)")
    plu_code: Mapped[str] = mapped_column(Text, comment="PLU Code(8||13)")
    inner_code: Mapped[str] = mapped_column(Text, comment="INNER Code(6)")
    name: Mapped[str] = mapped_column(Text, comment="商品名稱(30)")
    tax_flg: Mapped[str] = mapped_column(Text, comment="稅別(2)")
    type_1: Mapped[str] = mapped_column(Text, comment="商品區分１(2)")
    price: Mapped[str] = mapped_column(Text, comment="門市零售價(9)")
    pma_code: Mapped[str] = mapped_column(Text, comment="PMACode(2)")
    md_code: Mapped[str] = mapped_column(Text, comment="中分類Code(2)")
    sd_code: Mapped[str] = mapped_column(Text, comment="小分類Code(2)")
    m_code: Mapped[str] = mapped_column(Text, comment="MatrixCode(2)")
    sb_date_time: Mapped[str] = mapped_column(Text, comment="暫停銷售開始日時(12)")
    se_date_time: Mapped[str] = mapped_column(Text, comment="暫停銷售停止日時(12)")
    intl_code: Mapped[str] = mapped_column(Text, comment="單品條碼種類(1)")
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, comment="門市Code(6)")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")


class IfMntExt(Base):
    __tablename__ = "ifmntexts"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gmid: Mapped[str] = mapped_column(Text, comment="業務ID(5U,2)")
    mkbn: Mapped[str] = mapped_column(Text, comment="Maintenance區分(1)")
    plu_code: Mapped[str] = mapped_column(Text, comment="PLU Code(8||13)")
    inner_code: Mapped[str] = mapped_column(Text, comment="INNER Code(6)")
    name: Mapped[str] = mapped_column(Text, comment="商品名稱(30)")
    tax_flg: Mapped[str] = mapped_column(Text, comment="稅別(2)")
    type_1: Mapped[str] = mapped_column(Text, comment="商品區分１(2)")
    price: Mapped[str] = mapped_column(Text, comment="門市零售價(9)")
    pma_code: Mapped[str] = mapped_column(Text, comment="PMACode(2)")
    md_code: Mapped[str] = mapped_column(Text, comment="中分類Code(2)")
    sd_code: Mapped[str] = mapped_column(Text, comment="小分類Code(2)")
    m_code: Mapped[str] = mapped_column(Text, comment="MatrixCode(2)")
    sb_date_time: Mapped[str] = mapped_column(Text, comment="暫停銷售開始日時(12)")
    se_date_time: Mapped[str] = mapped_column(Text, comment="暫停銷售停止日時(12)")
    intl_code: Mapped[str] = mapped_column(Text, comment="單品條碼種類(1)")
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, comment="門市Code(6)")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")


class IfBookm(Base):
    __tablename__ = "ifbookms"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gmid: Mapped[str] = mapped_column(Text, comment="業務ID(2)")
    plu_code: Mapped[str] = mapped_column(Text, comment="PLU Code(13)")
    s_plu_code: Mapped[str] = mapped_column(Text, comment="第２段 Code(13)")
    name: Mapped[str] = mapped_column(Text, comment="PLU名稱(30)")
    price: Mapped[str] = mapped_column(Text, comment="單價(9)")
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, comment="門市Code(6)")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")


class IfNotDis(Base):
    __tablename__ = "ifnotdis"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gmid: Mapped[str] = mapped_column(Text, comment="業務ID(2)")
    start_date: Mapped[str] = mapped_column(Text, comment="開始日(8)")
    end_date: Mapped[str] = mapped_column(Text, comment="開始日(8)")
    unit_type: Mapped[str] = mapped_column(Text, comment="不可折扣類型(1)")
    pma_code: Mapped[str] = mapped_column(Text, comment="PMA(2)")
    m_code: Mapped[str] = mapped_column(Text, comment="中分類(2)")
    item_no: Mapped[str] = mapped_column(Text, comment="單品(6)")
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, comment="門市Code(6)")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")


class IfTouchP(Base):
    __tablename__ = "iftouchps"

    uuid: Mapped[str] = mapped_column(String(32), primary_key=True)
    gmid: Mapped[str] = mapped_column(Text, comment="業務ID(06,2)")
    touch_id: Mapped[str] = mapped_column(Text, comment="TouchＮｏ(2)")
    display_no: Mapped[str] = mapped_column(Text, comment="表示No(2)")
    pflg: Mapped[str] = mapped_column(Text, comment="Panel區分(1)")
    plu_code: Mapped[str] = mapped_column(Text, comment="PLUCode(13)")
    disp_name_1: Mapped[str] = mapped_column(Text, comment="表示名稱第一段(10)")
    disp_name_2: Mapped[str] = mapped_column(Text, comment="表示名稱第二段(10)")
    storeId: Mapped[Optional[str]] = mapped_column(String(6), nullable=True, comment="門市Code(6)")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Soft delete timestamp")
