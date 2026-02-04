"""
訂單狀態反查命令

CLI 入口點，使用 DI Container 注入 Service
"""
import typer
import logging
import json
import asyncio
from typing import Optional
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.icp_service import IcpService
from app.services.charge_status_service import ChargeStatusService

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
@inject
def charge_status(
    order_id: str = typer.Argument(..., help="訂單編號"),
    pay_type: Optional[str] = typer.Argument(None, help="付款方式 (ICP / CTBC)"),
    charge_status_service: ChargeStatusService = Provide[Container.charge_status_service],
    icp_service: IcpService = Provide[Container.icp_service],
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
        if pay_type == 'ICP':
            response = await icp_service.get_trade_status(order_id)
            if response.success:
                output_data = response.data if response.data else response.raw_response
                return json.dumps(output_data, ensure_ascii=False)
            else:
                return f"Failed: {response.error}"
        else:
            if pay_type == 'CTBC':
                response = await charge_status_service.process_ctbc(order_id)
            else:
                response = await charge_status_service.process(order_id)
            
            if response.success:
                return response.raw_response
            else:
                return f"Failed: {response.error}"

    try:
        final_result = asyncio.run(run_async_logic())
        typer.echo(f"反查結果-{order_id}: {final_result}")
        logger.info(f"反查結果-{order_id}", extra={'result': final_result})

    except Exception as e:
        logger.error("訂單反查錯誤", extra={
            'order_id': order_id,
            'error': str(e)
        })
        typer.secho(f"訂單反查發生錯誤: {e}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
