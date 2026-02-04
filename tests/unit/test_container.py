"""
DI Container 單元測試

測試 Container 的依賴注入功能
"""
import pytest
from unittest.mock import MagicMock, patch


class TestContainer:
    """測試 DI Container"""

    def test_container_provides_encryption_service(self):
        """
        場景：透過 Container 取得 EncryptionService
        預期：應該取得 Singleton 實例
        """
        # Given
        from app.core.container import Container
        container = Container()
        
        # When
        service1 = container.encryption_service()
        service2 = container.encryption_service()
        
        # Then
        assert service1 is not None
        assert service1 is service2  # Singleton

    def test_container_provides_icp_service(self):
        """
        場景：透過 Container 取得 IcpService
        預期：IcpService 應該已注入 EncryptionService
        """
        # Given
        from app.core.container import Container
        container = Container()
        
        # When
        service = container.icp_service()
        
        # Then
        assert service is not None
        assert hasattr(service, 'encryption_service')
        assert service.encryption_service is not None

    @pytest.mark.asyncio
    async def test_container_provides_async_db_session(self):
        """
        場景：Container 提供正確的資料庫連線
        預期：取得有效的 AsyncSession
        """
        # Given
        from app.core.container import Container
        container = Container()
        
        # When
        session = await container.db_session()
        
        # Then
        assert session is not None
        
        # 清理
        await container.db_session.shutdown()

    @pytest.mark.asyncio
    async def test_container_charge_status_service_with_session(self):
        """
        場景：透過 Container 取得 ChargeStatusService (含 DB Session)
        預期：Service 應該已注入 Repository
        """
        # Given
        from app.core.container import Container
        container = Container()
        
        # When
        service = await container.charge_status_service()
        
        # Then
        assert service is not None
        assert hasattr(service, 'order_repo')
        assert service.order_repo is not None
        
        # 清理
        await container.db_session.shutdown()
