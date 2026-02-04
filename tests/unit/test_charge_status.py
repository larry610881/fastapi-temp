"""
訂單狀態反查服務單元測試

測試 ChargeStatusService 與 IcpService 的核心功能
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
import json
import base64

from app.services.charge_status_service import ChargeStatusService
from app.services.icp_service import IcpService
from app.models.order import Order
from app.models.order_status import OrderStatus
from app.schemas.charge_status import ChargeStatusResponse


@pytest.fixture(autouse=True)
def mock_settings():
    """模擬設定以避免環境問題"""
    with patch('app.services.charge_status_service.settings') as s1, \
         patch('app.services.icp_service.settings') as s2:
        
        for s in [s1, s2]:
            s.CHARGE_APP_STATUS_URL = "http://op-api.test/status"
            s.ONLINE_PAY_MERCHANT_KEY = "dummy_key"
            s.ONLINE_PAY_CORPORATE_ID = "dummy_corp_id"
            s.ONLINE_PAY_AUTH_PAY = "dummy_auth"
            s.ONLINE_PAY_ENTRY_MODE = "dummy_mode"
            s.ONLINE_PAY_CORP_ID = "dummy_corp_id"
            s.GET_CTBC_OPW_PAYMENT_API_URL = "http://ctbc-api.test/"
            
            s.ICP_ENC_KEY_ID = "key"
            s.ICP_TIMEOUT = 10
            s.ICP_API_BASE_URL = "http://icp.test/"
            s.ICP_PLATFORM_ID = "pid"
            s.ICP_MERCHANT_ID = "mid"
        
        yield (s1, s2)


@pytest.fixture
def mock_order_repo():
    """模擬訂單 Repository"""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def mock_order_status_repo():
    """模擬訂單狀態 Repository"""
    repo = MagicMock()
    repo.get_by_order_id = AsyncMock()
    return repo


@pytest.fixture
def charge_status_service(mock_order_repo, mock_order_status_repo):
    """建立 ChargeStatusService 實例"""
    return ChargeStatusService(
        order_repo=mock_order_repo,
        order_status_repo=mock_order_status_repo
    )


@pytest.fixture
def mock_encryption_service():
    """模擬加密服務"""
    service = MagicMock()
    service.aes_encrypt.return_value = b"encrypted_content"
    service.rsa_sign.return_value = "signature"
    service.verify_signature.return_value = True
    service.aes_decrypt.return_value = json.dumps({"RtnCode": 1, "TradeStatus": 1})
    return service


@pytest.fixture
def icp_service(mock_encryption_service):
    """建立 IcpService 實例"""
    return IcpService(mock_encryption_service)


# ==========================================
# TEST: ChargeStatusService (OP)
# ==========================================

@pytest.mark.asyncio
async def test_charge_status_process_success(charge_status_service, mock_order_repo):
    """
    場景：成功查詢 OP 訂單狀態
    """
    # Given
    order_id = "ORD-2023-002"
    mock_order = Order(id=order_id, payable_amount=100, created_at=datetime(2023, 1, 1, 12, 0, 0))
    mock_order_repo.get_by_id.return_value = mock_order

    with patch.object(charge_status_service, '_post_with_retry') as mock_post:
        mock_response = MagicMock()
        mock_response.text = "1|OK"
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # When
        result = await charge_status_service.process(order_id)
        
        # Then
        assert isinstance(result, ChargeStatusResponse)
        assert result.success is True
        assert result.gateway == "OP"
        assert result.raw_response == "1|OK"
        mock_order_repo.get_by_id.assert_called_with(order_id)


@pytest.mark.asyncio
async def test_charge_status_process_order_not_found(charge_status_service, mock_order_repo):
    """
    場景：查無訂單
    """
    # Given
    order_id = "ORD-NON-EXISTENT"
    mock_order_repo.get_by_id.return_value = None

    # When
    result = await charge_status_service.process(order_id)

    # Then
    assert isinstance(result, ChargeStatusResponse)
    assert result.success is False
    assert "not found" in result.error.lower()


@pytest.mark.asyncio
async def test_charge_status_process_ctbc_success(
    charge_status_service, 
    mock_order_repo, 
    mock_order_status_repo
):
    """
    場景：查詢 CTBC 訂單狀態
    """
    # Given
    order_id = "ORD-CTBC-001"
    mock_order = Order(id=order_id, payable_amount=200, created_at=datetime.now())
    mock_status = OrderStatus(order_id=order_id, status='1', content=json.dumps({"walletSeq": "WS123"}))
    
    mock_order_repo.get_by_id.return_value = mock_order
    mock_order_status_repo.get_by_order_id.return_value = mock_status
    
    with patch.object(charge_status_service, '_get_with_retry') as mock_get:
        mock_response = MagicMock()
        mock_response.text = "OK"
        mock_get.return_value = mock_response
        
        # When
        result = await charge_status_service.process_ctbc(order_id)
        
        # Then
        assert isinstance(result, ChargeStatusResponse)
        assert result.success is True
        assert result.gateway == "CTBC"
        assert result.raw_response == "OK"


# ==========================================
# TEST: IcpService
# ==========================================

@pytest.mark.asyncio
async def test_icp_get_trade_status_success(icp_service):
    """
    場景：成功查詢 ICP 訂單狀態
    """
    # Given
    order_id = "ORD-2023-001"
    
    with patch.object(icp_service, '_post_with_retry') as mock_post:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.status_code = 200
        mock_response.headers = {'X-iCP-Signature': 'valid_sig'}
        mock_response.text = json.dumps({
            'RtnCode': 1, 
            'EncData': base64.b64encode(b"encrypted_resp").decode('utf-8')
        })
        mock_post.return_value = mock_response
        
        # When
        result = await icp_service.get_trade_status(order_id)
        
        # Then
        assert isinstance(result, ChargeStatusResponse)
        assert result.success is True
        assert result.gateway == "ICP"
        assert result.data['RtnCode'] == 1


@pytest.mark.asyncio
async def test_icp_get_trade_status_empty_order_id(icp_service):
    """
    場景：訂單編號為空
    """
    # When
    result = await icp_service.get_trade_status("")
    
    # Then
    assert isinstance(result, ChargeStatusResponse)
    assert result.success is False
    assert "空" in result.error
