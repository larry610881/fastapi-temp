"""
ICP 金流服務

提供 ICP API 呼叫、加解密、簽章驗證等功能
"""
import json
import logging
import base64
from typing import Dict, Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.config import settings
from app.services.encryption_service import EncryptionService
from app.schemas.charge_status import ChargeStatusResponse

logger = logging.getLogger(__name__)


class IcpService:
    """ICP 金流服務"""
    
    def __init__(self, encryption_service: EncryptionService):
        self.encryption_service = encryption_service

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True
    )
    async def _post_with_retry(
        self, 
        url: str, 
        data: Dict, 
        headers: Dict, 
        timeout: int
    ) -> httpx.Response:
        """帶重試機制的 POST 請求"""
        async with httpx.AsyncClient(timeout=timeout) as client:
            return await client.post(url, data=data, headers=headers)

    async def post_data_to_icp(
        self, 
        api_url: str, 
        signature: str, 
        enc_data: str, 
        arr_other_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        POST 資料到 ICP API
        
        Args:
            api_url: API URL
            signature: RSA 簽章
            enc_data: AES 加密資料 (Base64)
            arr_other_data: 其他附加資料
            
        Returns:
            API 回應
        """
        if arr_other_data is None:
            arr_other_data = {}
            
        enc_key_id = settings.ICP_ENC_KEY_ID
        timeout = settings.ICP_TIMEOUT

        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'X-iCP-EncKeyID': enc_key_id,
                'X-iCP-Signature': signature
            }

            payload = {
                'EncData': enc_data,
                **arr_other_data
            }

            logger.info(f"Posting to ICP: {api_url}")
            
            response = await self._post_with_retry(api_url, payload, headers, timeout)
            
            logger.info("ICP API Response Status", extra={
                'status': response.status_code,
                'url': api_url,
                'enc_key_id': enc_key_id
            })

            if not response.is_success:
                return {'error': f"ICP API 請求失敗，HTTP狀態碼: {response.status_code}"}

            return {
                'body': response.text,
                'headers': response.headers,
                'status': response.status_code
            }

        except httpx.TimeoutException as e:
            logger.error('ICP API 請求逾時', extra={
                'error': str(e),
                'url': api_url,
                'enc_key_id': enc_key_id
            })
            return {'error': f'ICP API 請求逾時: {str(e)}'}
        except httpx.ConnectError as e:
            logger.error('ICP API 連線錯誤', extra={
                'error': str(e),
                'url': api_url,
                'enc_key_id': enc_key_id
            })
            return {'error': f'ICP API 連線錯誤: {str(e)}'}
        except Exception as e:
            logger.error('ICP API 請求錯誤', extra={
                'error': str(e),
                'url': api_url,
                'enc_key_id': enc_key_id
            })
            return {'error': f'ICP API 請求錯誤: {str(e)}'}

    def parse_response(self, response_body: str) -> Dict[str, Any]:
        """
        解析 API 回應
        
        Args:
            response_body: API 回應內容
            
        Returns:
            解析後的資料
        """
        try:
            response_data = json.loads(response_body)

            if 'EncData' not in response_data:
                return response_data

            enc_data = base64.b64decode(response_data['EncData'])
            decrypted_data = self.encryption_service.aes_decrypt(enc_data)
            
            if isinstance(decrypted_data, dict) and 'error' in decrypted_data:
                return decrypted_data

            try:
                decrypted_json = json.loads(decrypted_data)
                response_data['decryptedEncData'] = decrypted_json
            except json.JSONDecodeError:
                response_data['decryptedEncData'] = decrypted_data

            return response_data

        except json.JSONDecodeError as e:
            logger.error('解析 API 回應 JSON 失敗', extra={'error': str(e), 'response': response_body})
            return {'error': f'解析 API 回應 JSON 失敗: {str(e)}'}
        except Exception as e:
            logger.error('解析 API 回應失敗', extra={'error': str(e), 'response': response_body})
            return {'error': f'解析 API 回應失敗: {str(e)}'}

    async def call_icp_api(
        self, 
        api_url: str, 
        data: Dict[str, Any], 
        arr_other_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        完整的 ICP API 呼叫流程
        
        Args:
            api_url: API URL
            data: 請求資料
            arr_other_data: 其他附加資料
            
        Returns:
            API 回應
        """
        if arr_other_data is None:
            arr_other_data = {}
            
        if not api_url:
            return {'error': f'API URL 不能為空, api_url: {api_url}'}

        if not api_url.startswith('http'):
            return {'error': f'API URL 格式不正確, api_url: {api_url}'}

        logger.info('開始呼叫 ICP API', extra={
            'api_url': api_url,
            'data_keys': list(data.keys()),
            'other_data_keys': list(arr_other_data.keys())
        })

        try:
            # 1. JSON Encode
            json_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            
            # 2. AES Encrypt
            encrypted_data = self.encryption_service.aes_encrypt(json_data)
            if isinstance(encrypted_data, dict) and 'error' in encrypted_data:
                logger.error('AES 加密失敗', extra={'error': encrypted_data['error']})
                return encrypted_data
                
            enc_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')

            # 3. RSA Sign
            signature = self.encryption_service.rsa_sign(enc_data_b64)
            if isinstance(signature, dict) and 'error' in signature:
                logger.error('RSA 簽名失敗', extra={'error': signature['error']})
                return signature

            # 4. Send Request
            response = await self.post_data_to_icp(api_url, signature, enc_data_b64, arr_other_data)
            
            if 'error' in response:
                return response
            
            response_body_str = response['body']
            arr_response_body = json.loads(response_body_str)
            
            if str(arr_response_body.get('RtnCode')) != '1':
                logger.error(f"api_url: {api_url} 回應錯誤", extra={
                    'RtnCode': arr_response_body.get('RtnCode'),
                    'RtnMsg': arr_response_body.get('RtnMsg')
                })
                return {
                    'error': f"ICP API 回應代碼 {arr_response_body.get('RtnCode')}: {arr_response_body.get('RtnMsg')}"
                }

            # 5. Verify Signature
            resp_headers = response['headers']
            x_icp_signature = resp_headers.get('X-iCP-Signature') or resp_headers.get('x-icp-signature')
            
            if x_icp_signature:
                is_valid = self.encryption_service.verify_signature(response_body_str, x_icp_signature)
                
                if not is_valid:
                    logger.error(f"api_url: {api_url} 回應簽名驗證失敗")
                    return {'error': '回應簽名驗證失敗'}
                
                logger.info(f"api_url: {api_url} 回應簽名驗證成功")
                
                # 6. Parse and Decrypt
                return self.parse_response(response_body_str)
            else:
                logger.error(f"api_url: {api_url} 回應簽名驗證失敗 (Missing Header)")
                return {'error': '回應簽名驗證失敗'}

        except json.JSONDecodeError as e:
            logger.error('ICP API 回應 JSON 解析失敗', extra={'api_url': api_url, 'error': str(e)})
            return {'error': f'ICP API 回應 JSON 解析失敗: {str(e)}'}
        except Exception as e:
            logger.error('ICP API 呼叫失敗', extra={'api_url': api_url, 'error': str(e)})
            return {'error': str(e)}

    async def get_trade_status(self, order_id: str) -> ChargeStatusResponse:
        """
        用訂單編號查詢 ICP 訂單狀態
        
        Args:
            order_id: 訂單編號
            
        Returns:
            ChargeStatusResponse
        """
        icpo_005_api = f"{settings.ICP_API_BASE_URL}ICPO005"
        
        try:
            if not order_id:
                raise ValueError('訂單編號不能為空')

            data = {
                'PlatformID': settings.ICP_PLATFORM_ID,
                'MerchantID': settings.ICP_MERCHANT_ID,
                'MerchantTradeNo': str(order_id)
            }

            response = await self.call_icp_api(icpo_005_api, data)
            
            logger.info('ICP 訂單反查完成', extra={'order_id': order_id, 'success': 'error' not in response})
            
            if 'error' in response:
                return ChargeStatusResponse(
                    success=False, 
                    order_id=order_id, 
                    gateway="ICP", 
                    error=response['error']
                )

            return ChargeStatusResponse(
                success=True, 
                order_id=order_id, 
                gateway="ICP", 
                data=response.get('decryptedEncData'),
                raw_response=response.get('body')
            )

        except ValueError as e:
            logger.error('ICP 訂單反查參數錯誤', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="ICP", 
                error=str(e)
            )
        except Exception as e:
            logger.error('ICP 訂單反查異常', extra={'order_id': order_id, 'error': str(e)})
            return ChargeStatusResponse(
                success=False, 
                order_id=order_id, 
                gateway="ICP", 
                error=str(e)
            )
