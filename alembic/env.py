import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 導入專案設定與 MetaData
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.order_status import OrderStatus
from app.models.order_short_key import OrderShortKey
from app.models.store import Store
from app.models.if_tables import IfContrl, IfPluExt, IfMntExt, IfBookm, IfNotDis, IfTouchP
from app.models.auth_tables import Permission, Role, model_has_roles, model_has_permissions, role_has_permissions
from app.models.failed_job import FailedJob
from app.models.page_manager import PageManager
from app.models.websockets_statistics_entry import WebsocketsStatisticsEntry
from app.models.financial_tables import (
    BmsConsolidateFile, BmsDetailFile,
    CathaySettleConsolidateFile, CathaySettleDetailFile, CathayDiffConsolidateFile, CathayDiffDetailFile,
    IcpSettleConsolidateFile, IcpSettleDetailFile, IcpDiffConsolidateFile, IcpDiffDetailFile,
    PayUniSettleConsolidateFile, PayUniSettleDetailFile, PayUniDiffConsolidateFile, PayUniDiffDetailFile
)
from app.models.sc_host import SendToSCHostData, SendToSCHostDailyData
from app.models.checkout import CheckoutSmsConsolidateFile, CheckoutSmsDetailFile, CheckoutPayuniCredithash

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 動態設定資料庫 URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 客製化 target_metadata
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and reflected and compare_to is None:
        return False
    return True

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
