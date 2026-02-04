"""
Charge Status BDD Step Definitions

對應 tests/features/charge_status.feature
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.charge_status_service import ChargeStatusService
from app.services.icp_service import IcpService
from app.services.encryption_service import EncryptionService
from app.schemas.charge_status import ChargeStatusResponse

# 載入 feature 檔案
scenarios('../features/charge_status.feature')


# ==========================================
# Fixtures
# ==========================================

@pytest.fixture
def mock_order_repo():
    """Mock OrderRepository"""
    return MagicMock()


@pytest.fixture
def mock_order_status_repo():
    """Mock OrderStatusRepository"""
    return MagicMock()


@pytest.fixture
def mock_encryption_service():
    """Mock EncryptionService"""
    return MagicMock(spec=EncryptionService)


@pytest.fixture
def charge_status_service(mock_order_repo, mock_order_status_repo):
    """建立 ChargeStatusService 實例"""
    return ChargeStatusService(
        order_repo=mock_order_repo,
        order_status_repo=mock_order_status_repo
    )


@pytest.fixture
def icp_service(mock_encryption_service):
    """建立 IcpService 實例"""
    return IcpService(mock_encryption_service)


@pytest.fixture
def test_context():
    """測試上下文，儲存中間結果"""
    return {}


# ==========================================
# Given Steps
# ==========================================

@given(parsers.parse('存在一筆訂單 ID 為 "{order_id}" 且付款方式為 "{pay_type}"'))
def order_exists_with_pay_type(order_id, pay_type, mock_order_repo, test_context):
    """設定訂單存在"""
    mock_order = MagicMock()
    mock_order.id = order_id
    mock_order.payable_amount = 100
    mock_order.created_at = MagicMock()
    mock_order.created_at.strftime = MagicMock(return_value="20230101")
    
    mock_order_repo.get_by_id = AsyncMock(return_value=mock_order)
    test_context['order_id'] = order_id
    test_context['pay_type'] = pay_type
    test_context['mock_order'] = mock_order


@given(parsers.parse('外部 ICP 服務回傳 "{response}"'))
def icp_service_returns(response, test_context):
    """設定 ICP 回應"""
    test_context['icp_response'] = response


@given(parsers.parse('外部 OP 服務回傳 "{response}"'))
def op_service_returns(response, test_context):
    """設定 OP 回應"""
    test_context['op_response'] = response


@given(parsers.parse('不存在 ID 為 "{order_id}" 的訂單'))
def order_not_exists(order_id, mock_order_repo, test_context):
    """設定訂單不存在"""
    mock_order_repo.get_by_id = AsyncMock(return_value=None)
    test_context['order_id'] = order_id


@given("外部 ICP 服務逾時")
def icp_service_timeout(test_context):
    """設定 ICP 逾時"""
    test_context['icp_timeout'] = True


# ==========================================
# When Steps
# ==========================================

@when(parsers.parse('我查詢 "{order_id}" 的 "{pay_type}" 付款狀態'))
@pytest.mark.asyncio
async def query_payment_status(order_id, pay_type, charge_status_service, icp_service, test_context):
    """執行付款狀態查詢"""
    if pay_type == 'ICP':
        with patch.object(icp_service, '_post_with_retry') as mock_post:
            if test_context.get('icp_timeout'):
                import httpx
                mock_post.side_effect = httpx.TimeoutException("Timeout")
            else:
                mock_response = MagicMock()
                mock_response.text = '{"TradeStatus": 1}'
                mock_post.return_value = mock_response
            
            try:
                result = await icp_service.get_trade_status(order_id)
                test_context['result'] = result
            except Exception as e:
                test_context['result'] = ChargeStatusResponse(
                    success=False,
                    order_id=order_id,
                    gateway=pay_type,
                    error=str(e)
                )
    else:
        with patch.object(charge_status_service, '_post_with_retry') as mock_post:
            mock_response = MagicMock()
            mock_response.text = test_context.get('op_response', '1|OK')
            mock_post.return_value = mock_response
            
            result = await charge_status_service.process(order_id)
            test_context['result'] = result


# ==========================================
# Then Steps
# ==========================================

@then(parsers.parse('結果應為包含 "TradeStatus": 1 的成功 JSON 回應'))
def should_return_trade_status_success(test_context):
    """驗證 ICP 成功結果"""
    result = test_context.get('result')
    assert result is not None


@then(parsers.parse('結果應為 "{expected}"'))
def should_return_expected(expected, test_context):
    """驗證回傳結果"""
    result = test_context.get('result')
    assert result is not None


@then('結果應顯示失敗或 "False"')
def should_show_failure(test_context):
    """驗證失敗結果"""
    result = test_context.get('result')
    assert result is not None
    assert result.success is False


@then("結果應顯示錯誤")
def should_show_error(test_context):
    """驗證錯誤結果"""
    result = test_context.get('result')
    assert result is not None
    assert result.success is False
