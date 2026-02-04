"""
依賴注入容器

統一管理 Service、Repository 與資料庫連線的生命週期
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from dependency_injector import containers, providers

from app.db.session import SessionLocal, AsyncSession
from app.repositories.order_repository import OrderRepository
from app.repositories.order_status_repository import OrderStatusRepository
from app.services.encryption_service import EncryptionService
from app.services.icp_service import IcpService
from app.services.charge_status_service import ChargeStatusService


@asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:
    """提供 Async DB Session 的 Context Manager"""
    async with SessionLocal() as session:
        yield session  # async with 結束時自動 close，無需手動呼叫


class Container(containers.DeclarativeContainer):
    """應用程式依賴注入容器"""
    
    # 配置
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.commands.charge_status",
            "app.api.v1.endpoints.health",
        ]
    )
    
    # 資料庫 Session (每次請求獨立)
    db_session = providers.Resource(
        get_db_session
    )
    
    # Repositories
    order_repo = providers.Factory(
        OrderRepository,
        db=db_session
    )
    
    order_status_repo = providers.Factory(
        OrderStatusRepository,
        db=db_session
    )
    
    # Services
    encryption_service = providers.Singleton(
        EncryptionService
    )
    
    icp_service = providers.Factory(
        IcpService,
        encryption_service=encryption_service
    )
    
    charge_status_service = providers.Factory(
        ChargeStatusService,
        order_repo=order_repo,
        order_status_repo=order_status_repo
    )
