"""
訂單狀態反查服務

提供 OP 與 CTBC 訂單狀態查詢功能
"""
import json
import logging
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.config import settings
from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.repositories.order_status_repository import OrderStatusRepository
from app.schemas.charge_status import ChargeStatusResponse

logger = logging.getLogger(__name__)


class ChargeStatusService:
    """訂單狀態反查服務"""
    
    def __init__(
        self, 
        order_repo: OrderRepository, 
        order_status_repo: Optional[OrderStatusRepository] = None
    ):
        """
        Args:
            order_repo: 訂單 Repository
            order_status_repo: 訂單狀態 Repository (CTBC 查詢時需要)
        """
        self.order_repo = order_repo
        self.order_status_repo = order_status_repo

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True
    )
    async def _post_with_retry(self, url: str, payload: Dict, headers: Dict) -> httpx.Response:
        """帶重試機制的 POST 請求"""
        async with httpx.AsyncClient(timeout=30) as client:
            return await client.post(url, json=payload, headers=headers)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True
    )
    async def _get_with_retry(self, url: str, headers: Dict) -> httpx.Response:
        """帶重試機制的 GET 請求"""
        async with httpx.AsyncClient(timeout=30) as client:
            return await client.get(url, headers=headers)

    async def process(self, order_id: str) -> ChargeStatusResponse:
        """
        反查國泰訂單資訊 (OP)
        
        Args:
            order_id: 訂單編號
            
        Returns:
            ChargeStatusResponse
        """
        try:
            order = await self.order_repo.get_by_id(order_id)
            
            if not order:
                logger.error(f"Order not found: {order_id}")
                return ChargeStatusResponse(
                    success=False, 
                    order_id=order_id, 
                    gateway="OP", 
                    error="Order not found"
                )

            trans_name = f'OP錢包x-store訂單編號{order_id}'
            created_at = order.created_at
            
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)

            merchant_trade_date = created_at.strftime('%Y%m%d')
            merchant_trade_time = created_at.strftime('%H%M%S')
            amount = int(float(order.payable_amount) * 100)

            payload = {
                "merchantKey": settings.ONLINE_PAY_MERCHANT_KEY,
                "corporateId": settings.ONLINE_PAY_CORPORATE_ID,
                "merchantTradeNo": str(order_id),
                "authParty": settings.ONLINE_PAY_AUTH_PAY,
                "entryMode": settings.ONLINE_PAY_ENTRY_MODE,
                "transName": trans_name,
                "amount": amount,
                "merchantTradeDate": merchant_trade_date,
                "merchantTradeTime": merchant_trade_time
            }

            headers = {'Content-Type': 'application/json'}
            url = settings.CHARGE_APP_STATUS_URL

            response = await self._post_with_retry(url, payload, headers)
            result = response.text

            logger.info('訂單反查成功', extra={'order_id': order_id, 'res': result})
            return ChargeStatusResponse(
                success=True, 
                order_id=order_id, 
                gateway="OP", 
                raw_response=result
            )

        except httpx.TimeoutException as e:
            logger.error('訂單反查逾時', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="OP", 
                error=f"Request timeout: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            logger.error('訂單反查 HTTP 錯誤', extra={'order_id': order_id, 'status': e.response.status_code})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="OP", 
                error=f"HTTP Error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error('訂單反查異常', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="OP", 
                error=str(e)
            )

    async def process_ctbc(self, order_id: str, trade_type: int = 1) -> ChargeStatusResponse:
        """
        查詢 CTBC 訂單資訊
        
        Args:
            order_id: 訂單編號
            trade_type: 交易類型 (預設 1)
            
        Returns:
            ChargeStatusResponse
        """
        if not self.order_status_repo:
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="CTBC", 
                error="OrderStatusRepository not provided"
            )
            
        try:
            order_info = await self.order_repo.get_by_id(order_id)
            order_status_info = await self.order_status_repo.get_by_order_id(order_id, '1')

            if not order_info:
                logger.error(f"查無此訂單：{order_id}")
                return ChargeStatusResponse(
                    success=False, 
                    order_id=order_id, 
                    gateway="CTBC", 
                    error="Order not found"
                )

            if not order_status_info:
                logger.error(f"此訂單無任何狀態紀錄：{order_id}")
                return ChargeStatusResponse(
                    success=False, 
                    order_id=order_id, 
                    gateway="CTBC", 
                    error="Order status not found"
                )

            try:
                order_content = json.loads(order_status_info.content) if isinstance(
                    order_status_info.content, str
                ) else order_status_info.content
            except (json.JSONDecodeError, TypeError):
                order_content = {}

            payment_content = {
                'corpID': settings.ONLINE_PAY_CORP_ID,
                'merchantTradeNo': str(order_id),
                'bankSeq': str(order_id),
                'amount': order_info.payable_amount,
                'walletSeq': order_content.get('walletSeq'),
                'tradeType': trade_type,
            }

            filtered = {k: v for k, v in payment_content.items() if v is not None and v != ''}
            query_string = urllib.parse.urlencode(filtered)
            
            base_url = settings.GET_CTBC_OPW_PAYMENT_API_URL
            if not base_url.endswith('/'):
                base_url += '/'
            
            opw_url = f"{base_url}order_query?{query_string}"
            headers = {'Accept': 'application/json'}
            
            response = await self._get_with_retry(opw_url, headers)
            result = response.text

            logger.info('OPW_CTBC 訂單反查成功', extra={'order_id': order_id, 'res': result})
            return ChargeStatusResponse(
                success=True, 
                order_id=order_id, 
                gateway="CTBC", 
                raw_response=result
            )
            
        except httpx.TimeoutException as e:
            logger.error('CTBC 訂單反查逾時', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="CTBC", 
                error=f"Request timeout: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            logger.error('CTBC 訂單反查 HTTP 錯誤', extra={'order_id': order_id, 'status': e.response.status_code})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="CTBC", 
                error=f"HTTP Error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error('CTBC 訂單反查異常', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="CTBC", 
                error=str(e)
            )
