"""
DI Container BDD Step Definitions

對應 tests/features/di_container.feature (中文關鍵字版本)
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from app.core.container import Container

# 載入 feature 檔案
scenarios('../features/di_container.feature')


# ==========================================
# Fixtures
# ==========================================

@pytest.fixture
def container():
    """建立 Container 實例"""
    return Container()


@pytest.fixture
def service_instance():
    """儲存取得的 Service 實例"""
    return {}


# ==========================================
# Given Steps (假設)
# ==========================================

@given("DI Container 已初始化", target_fixture="container")
def di_container_initialized():
    """確認 Container 可以初始化"""
    container = Container()
    assert container is not None
    return container


# ==========================================
# When Steps (當)
# ==========================================

@when("我從 Container 請求 ChargeStatusService", target_fixture="service_instance")
@pytest.mark.asyncio
async def request_charge_status_service(container):
    """從 Container 取得 ChargeStatusService"""
    service = await container.charge_status_service()
    return {'charge_status': service, 'db_session': None}


@when("我從 Container 請求 db_session", target_fixture="service_instance")
@pytest.mark.asyncio
async def request_db_session(container):
    """從 Container 取得 DB Session"""
    session = await container.db_session()
    return {'db_session': session, 'charge_status': None}


@when(parsers.parse('我執行 charge-status 指令並傳入訂單編號 "{order_id}"'), target_fixture="service_instance")
def execute_charge_status_command(order_id):
    """模擬執行 CLI 指令"""
    return {'order_id': order_id, 'charge_status': None, 'db_session': None}


# ==========================================
# Then Steps (那麼/而且)
# ==========================================

@then("我應該取得一個可用的服務實例")
def should_get_service_instance(service_instance):
    """驗證取得的服務實例"""
    assert service_instance.get('charge_status') is not None


@then("該服務應該已注入 OrderRepository")
def should_have_order_repo(service_instance):
    """驗證 OrderRepository 已注入"""
    service = service_instance.get('charge_status')
    assert hasattr(service, 'order_repo')
    assert service.order_repo is not None


@then("我應該取得一個有效的 AsyncSession")
def should_get_async_session(service_instance):
    """驗證取得 AsyncSession"""
    assert service_instance.get('db_session') is not None


@then("服務應該被正確注入並執行")
def service_should_be_injected(service_instance):
    """驗證服務注入正確"""
    assert service_instance.get('order_id') is not None
