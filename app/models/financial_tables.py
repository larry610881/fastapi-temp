from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, Float, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# === BMS ===
class BmsConsolidateFile(Base):
    __tablename__ = "b_m_s_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1), comment="檔頭標籤")
    time: Mapped[str] = mapped_column(String(14), comment="檔案時間")
    countSum: Mapped[int] = mapped_column(Integer, comment="總筆數")
    moneySum: Mapped[int] = mapped_column(Integer, comment="總金額")
    handlingFeeSum: Mapped[int] = mapped_column(Integer, comment="手續費總金額")
    originalContent: Mapped[str] = mapped_column(Text, comment="原始內容")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class BmsDetailFile(Base):
    __tablename__ = "b_m_s_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    discount_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    consumer_authentication_code: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    exchange_rate: Mapped[int] = mapped_column(Integer)
    transfer_amount: Mapped[int] = mapped_column(Integer)
    transaction_results_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reason_for_refund: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    handling_fee_amount: Mapped[float] = mapped_column(Float) # double
    general_handling_fee: Mapped[float] = mapped_column(Float) # double
    handling_fee_for_collection_amount: Mapped[float] = mapped_column(Float) # double
    proxy_sales_amount_handling_fee_amount: Mapped[float] = mapped_column(Float) # double
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    transaction_notes: Mapped[str] = mapped_column(String(1))
    order_number: Mapped[str] = mapped_column(String(32))

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

# === Cathay ===
class CathaySettleConsolidateFile(Base):
    __tablename__ = "cathay_settle_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    realAmount: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CathaySettleDetailFile(Base):
    __tablename__ = "cathay_settle_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    transaction_results_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bank_side_comparison_results: Mapped[str] = mapped_column(String(1))
    bank_side_comparison_result_code: Mapped[str] = mapped_column(String(5))
    bank_side_comparison_result_description: Mapped[str] = mapped_column(Text)
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CathayDiffConsolidateFile(Base):
    __tablename__ = "cathay_diff_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CathayDiffDetailFile(Base):
    __tablename__ = "cathay_diff_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    diff_type: Mapped[str] = mapped_column(String(1))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    consumer_authentication_code: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

# === ICP ===
class IcpSettleConsolidateFile(Base):
    __tablename__ = "i_c_p_settle_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    realAmount: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class IcpSettleDetailFile(Base):
    __tablename__ = "i_c_p_settle_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    transaction_results_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    icp_side_comparison_results: Mapped[str] = mapped_column(String(1))
    icp_side_comparison_result_code: Mapped[str] = mapped_column(String(5))
    icp_side_comparison_result_description: Mapped[str] = mapped_column(Text)
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class IcpDiffConsolidateFile(Base):
    __tablename__ = "i_c_p_diff_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class IcpDiffDetailFile(Base):
    __tablename__ = "i_c_p_diff_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    diff_type: Mapped[str] = mapped_column(String(1))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    consumer_authentication_code: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

# === PayUni ===
class PayUniSettleConsolidateFile(Base):
    __tablename__ = "p_a_y_u_ni_settle_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    realAmount: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class PayUniSettleDetailFile(Base):
    __tablename__ = "p_a_y_u_ni_settle_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    transaction_results_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bank_side_comparison_results: Mapped[str] = mapped_column(String(1))
    bank_side_comparison_result_code: Mapped[str] = mapped_column(String(5))
    bank_side_comparison_result_description: Mapped[str] = mapped_column(Text)
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class PayUniDiffConsolidateFile(Base):
    __tablename__ = "p_a_y_u_ni_diff_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    countSum: Mapped[int] = mapped_column(Integer)
    moneySum: Mapped[int] = mapped_column(Integer)
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class PayUniDiffDetailFile(Base):
    __tablename__ = "p_a_y_u_ni_diff_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    diff_type: Mapped[str] = mapped_column(String(1))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer)
    discount_amount: Mapped[int] = mapped_column(Integer)
    discount_point: Mapped[int] = mapped_column(Integer)
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    consumer_authentication_code: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer)
    collection_amount: Mapped[int] = mapped_column(Integer)
    proxySales_amount: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

# === CTBC ===
class CTBCSettleConsolidateFile(Base):
    __tablename__ = "c_t_b_c_settle_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1), comment="檔頭標籤")
    time: Mapped[str] = mapped_column(String(14), comment="檔案時間")
    countSum: Mapped[int] = mapped_column(Integer, default=0, comment="總筆數")
    moneySum: Mapped[int] = mapped_column(Integer, default=0, comment="總金額")
    realAmount: Mapped[int] = mapped_column(Integer, comment="撥款金額")
    start_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True, comment="撥款區間-起")
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True, comment="撥款區間-訖")
    bank_code: Mapped[str] = mapped_column(String(3), comment="銀行代碼")
    originalContent: Mapped[str] = mapped_column(Text, comment="彙整檔的原始內容")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CTBCSettleDetailFile(Base):
    __tablename__ = "c_t_b_c_settle_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    time: Mapped[str] = mapped_column(String(14))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28))
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    discount_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    discount_point: Mapped[int] = mapped_column(Integer) # unsignedInteger
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    transaction_results_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    collection_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    proxy_sales_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bank_side_comparison_results: Mapped[str] = mapped_column(String(1))
    bank_side_comparison_result_code: Mapped[str] = mapped_column(String(5))
    bank_side_comparison_result_description: Mapped[str] = mapped_column(Text)
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CTBCDiffConsolidateFile(Base):
    __tablename__ = "c_t_b_c_diff_consolidate_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1), comment="檔頭標籤")
    time: Mapped[str] = mapped_column(String(14), comment="檔案時間")
    countSum: Mapped[int] = mapped_column(Integer, default=0, comment="總筆數")
    moneySum: Mapped[int] = mapped_column(Integer, default=0, comment="總金額")
    bank_code: Mapped[str] = mapped_column(String(3), comment="銀行代碼")
    originalContent: Mapped[str] = mapped_column(Text)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class CTBCDiffDetailFile(Base):
    __tablename__ = "c_t_b_c_diff_detail_files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(1))
    diff_type: Mapped[str] = mapped_column(String(1))
    status: Mapped[str] = mapped_column(String(1))
    type: Mapped[str] = mapped_column(String(6))
    bank_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    order_id: Mapped[str] = mapped_column(String(28), comment="特店交易編號")
    o2oId: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    payment_institution_transaction_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    transaction_time: Mapped[Optional[str]] = mapped_column(String(14), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    transaction_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    discount_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    discount_point: Mapped[int] = mapped_column(Integer) # unsignedInteger
    coupon_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    terminal_code: Mapped[str] = mapped_column(String(3))
    consumer_authentication_code: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    general_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    collection_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    proxy_sales_amount: Mapped[int] = mapped_column(Integer) # unsignedInteger
    store_id: Mapped[str] = mapped_column(String(6))
    pos_id: Mapped[str] = mapped_column(String(2))
    cash_register_transaction_serial_number: Mapped[str] = mapped_column(String(6))
    bonus_activity_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    merchant_id: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
