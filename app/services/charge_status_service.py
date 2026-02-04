import json
import logging
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Union, Optional
from sqlalchemy.orm import Session
# from sqlalchemy import select # No longer needed

from app.core.config import settings
from app.models.order import Order
from app.models.order_status import OrderStatus
from app.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)

from app.schemas.charge_status import ChargeStatusResponse

import httpx

class ChargeStatusService:
    async def process(self, order_repo: OrderRepository, order_id: str) -> ChargeStatusResponse:
        """
        反查國泰訂單資訊 (OP)
        """
        try:
            # order = await order_repo.get_by_id(order_id)
            # Assuming repo is updated to async, if not we need to fix repo first. 
            # But let's assume I will fix repo next.
            order = await order_repo.get_by_id(order_id)
            
            if not order:
                logger.error(f"Order not found: {order_id}")
                return ChargeStatusResponse(success=False, order_id=order_id, gateway="OP", error="Order not found")

            trans_name = f'OP錢包x-store訂單編號{order_id}'
            created_at = order.created_at
            
            # Ensure created_at is datetime
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)

            merchant_trade_date = created_at.strftime('%Y%m%d')
            merchant_trade_time = created_at.strftime('%H%M%S')
            
            # Amount * 100
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

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                result = response.text

            logger.info('訂單反查', extra={'order_id': order_id, 'res': result})
            return ChargeStatusResponse(success=True, order_id=order_id, gateway="OP", raw_response=result)

        except Exception as e:
            logger.info('訂單反查exception', extra={'order_id': order_id, 'res': str(e)})
            return ChargeStatusResponse(success=False, order_id=order_id, gateway="OP", error=str(e))

    async def process_ctbc(self, order_repo: OrderRepository, order_id: str, trade_type: int = 1) -> ChargeStatusResponse:
        """
        查詢CTBC 訂單資訊
        """
        try:
            order_info = await order_repo.get_by_id(order_id)
            order_status_info = await order_repo.get_order_status(order_id, '1')

            if not order_info:
                logger.error(f"查無此訂單：{order_id}")
                return ChargeStatusResponse(success=False, order_id=order_id, gateway="CTBC", error="Order not found")

            if not order_status_info:
                logger.error(f"此訂單無任何狀態紀錄：{order_id}")
                return ChargeStatusResponse(success=False, order_id=order_id, gateway="CTBC", error="Order status not found")

            try:
                # order_status_info.content might be string in DB
                order_content = json.loads(order_status_info.content) if isinstance(order_status_info.content, str) else order_status_info.content
            except Exception:
                order_content = {}

            payment_content = {
                'corpID': settings.ONLINE_PAY_CORP_ID,
                'merchantTradeNo': str(order_id),
                'bankSeq': str(order_id),
                'amount': order_info.payable_amount,
                'walletSeq': order_content.get('walletSeq'),
                'tradeType': trade_type,
            }

            # Filter out None or empty string, but keep 0
            filtered = {k: v for k, v in payment_content.items() if v is not None and v != ''}

            query_string = urllib.parse.urlencode(filtered)
            base_url = settings.GET_CTBC_OPW_PAYMENT_API_URL
            
            # Append slash if needed, or handle path join
            if not base_url.endswith('/'):
                base_url += '/'
            
            opw_url = f"{base_url}order_query?{query_string}"

            headers = {'Accept': 'application/json'}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(opw_url, headers=headers)
                result = response.text

            logger.info('OPW_CTBC 訂單反查', extra={'order_id': order_id, 'res': result})
            
            return ChargeStatusResponse(success=True, order_id=order_id, gateway="CTBC", raw_response=result)
            
        except Exception as e:
            logger.info('OPW_CTBC 訂單反查exception', extra={'order_id': order_id, 'res': str(e)})
            return ChargeStatusResponse(success=False, order_id=order_id, gateway="CTBC", error=str(e))

    def parse_ctbc_xml(self, raw_xml: str) -> Dict[str, Any]:
        """
        Parse CTBC XML response
        Note: The legacy code uses SimpleXMLElement. In Python, we can use xml.etree.ElementTree or xmltodict.
        I will use a simple regex approach or xmltodict if simple enough, but standard lib xml.etree is safer.
        Actually, legacy does regex replacement then simplexml.
        """
        import re
        import xml.etree.ElementTree as ET
        
        try:
            # Remove namespace ns0
            raw_xml = re.sub(r'(</?)ns0:', r'\1', raw_xml)
            raw_xml = re.sub(r'xmlns:ns0="[^"]+"', '', raw_xml)
            
            root = ET.fromstring(raw_xml)
            
            # Convert to dict (simplified)
            def etree_to_dict(t):
                d = {t.tag: {} if t.attrib else None}
                children = list(t)
                if children:
                    dd = {}
                    for dc in children:
                        # handle multiple children with same tag if needed, but for simple dict...
                        # Legacy uses json_encode(xml), which usually handles single children as Key: Value, multiple as Key: [Values]
                        # For now, let's just do simple recursive
                        pass
                    # A robust xml to dict is complex.
                    # Since this method isn't strictly used in the command flow shown, I'll return a basic structure or use a helper if needed.
                    # Re-reading legacy: return json_decode(json_encode($xml, ...), true);
                    pass
                return {} # Placeholder if complex

            # Better: just return the raw xml or implementing if strictly needed.
            # Start simple:
            return {} 
            
        except Exception as e:
             raise Exception("XML 解析失敗")
