"""
訂單狀態反查命令

CLI 入口點，用於手動執行訂單狀態反查
"""
import typer
import logging
import json
import asyncio
from typing import Optional

from app.db.session import SessionLocal
from app.services.encryption_service import EncryptionService
from app.services.icp_service import IcpService
from app.services.charge_status_service import ChargeStatusService
from app.repositories.order_repository import OrderRepository
from app.repositories.order_status_repository import OrderStatusRepository

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def charge_status(
    order_id: str = typer.Argument(..., help="訂單編號"),
    pay_type: Optional[str] = typer.Argument(None, help="付款方式 (ICP / CTBC)")
):
    """
    訂單手動反查
    
    根據付款方式查詢訂單狀態：
    - ICP: 使用 ICP 金流 API
    - CTBC: 使用 CTBC OPW API
    - 預設: 使用 OP 錢包 API
    """
    typer.echo(f"訂單反查 {order_id}")

    async def run_async_logic():
        result = None
        
        if pay_type == 'ICP':
            # ICP 查詢不需要資料庫
            encryption_service = EncryptionService()
            icp_service = IcpService(encryption_service)
            response = await icp_service.get_trade_status(order_id)
            
            if response.success:
                output_data = response.data if response.data else response.raw_response
                result = json.dumps(output_data, ensure_ascii=False)
            else:
                result = f"Failed: {response.error}"
                
        else:
            # OP / CTBC 查詢需要資料庫
            async with SessionLocal() as session:
                order_repo = OrderRepository(session)
                order_status_repo = OrderStatusRepository(session)
                
                charge_status_service = ChargeStatusService(
                    order_repo=order_repo,
                    order_status_repo=order_status_repo
                )
                
                if pay_type == 'CTBC':
                    response = await charge_status_service.process_ctbc(order_id)
                else:
                    response = await charge_status_service.process(order_id)
                
                if response.success:
                    result = response.raw_response
                else:
                    result = f"Failed: {response.error}"
                    
        return result

    try:
        final_result = asyncio.run(run_async_logic())
        typer.echo(f"反查結果-{order_id}: {final_result}")
        logger.info(f"反查結果-{order_id}", extra={'result': final_result})

    except Exception as e:
        logger.error("訂單反查錯誤", extra={
            'order_id': order_id,
            'error': str(e)
        })
        typer.secho("訂單反查發生錯誤", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
