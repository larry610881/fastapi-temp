import typer
import logging
import json
from typing import Optional
from app.db.session import SessionLocal
from app.services.encryption_service import EncryptionService
from app.services.icp_service import IcpService
from app.services.charge_status_service import ChargeStatusService

app = typer.Typer()
logger = logging.getLogger(__name__)

@app.command()
def charge_status(
    order_id: str = typer.Argument(..., help="訂單編號"),
    pay_type: Optional[str] = typer.Argument(None, help="付款方式 (ICP)")
):
    """
    訂單手動反查
    """
    typer.echo(f"訂單反查 {order_id}")
    
    # The original `db = SessionLocal()` is removed here as the async logic will manage its own session.
    # If `get_db` was used via Typer's dependency injection, it would be a different approach.
    # For direct calls within the command, we manage the session explicitly.
    import asyncio

    async def run_async_logic():
        result = None
        
        if pay_type == 'ICP':
            encryption_service = EncryptionService()
            icp_service = IcpService(encryption_service)
            response = await icp_service.get_trade_status(order_id)
            
            if response.success:
                # Original behavior: dump the dict (decrypted data or raw response?)
                # Legacy: json.dumps(response, ...) where response was the dict from service
                # The service now returns .data (decrypted) and .raw_response (body)
                # If we want the full details like before:
                # The old service returned the whole dict including 'decryptedEncData'.
                # Let's reconstruct or just print data.
                # If 'data' is present, it's the decrypted content usually needed.
                output_data = response.data if response.data else response.raw_response
                result = json.dumps(output_data, ensure_ascii=False)
            else:
                result = f"Failed: {response.error}"
                
        else: # OP
            # Use Repository
            from app.repositories.order_repository import OrderRepository
            # Make sure to get an async db session if needed, 
            # OR refactor repo to init with session inside? 
            # Our OrderRepository takes `db: AsyncSession`.
            # The `db` injected by Typer depends on `get_db`.
            # `get_db` is an async generator.
            # We need to manually manage the session here if not provided by Dependency injection in a way Typer supports natively for async.
            # Typer doesn't support async/await natively on command functions easily properly without `asyncio.run`.
            # And handling `get_db` generator manually:
            # The `SessionLocal` imported at the top is assumed to be an async session factory now.
            
            async with SessionLocal() as session:
                order_repo = OrderRepository(session)
                charge_status_service = ChargeStatusService()
                
                # Check for CTBC
                # Logic: how to detect CTBC? old command just called process (OP).
                # New command might want to support both or auto-detect?
                # User didn't specify auto-detect logic. Sticking to OP default as per old code, or maybe CTBC if requested?
                # For now, default process() which is OP.
                
                response = await charge_status_service.process(order_repo, order_id)
                
                if response.success:
                    result = response.raw_response
                else:
                     result = f"Failed: {response.error}"
        return result

    try:
        # If DB dependency is needed for ICP (it wasn't used in ICP path above, but cleaner to verify),
        # ICP didn't use DB in original code.
        
        final_result = asyncio.run(run_async_logic())

        # Log to console as well
        typer.echo(f"反查結果-{order_id}: {final_result}")
        
        # Log via logger (assuming configured to similar channel or file)
        logger.info(f"反查結果-{order_id}", extra={'result': final_result})

    except Exception as e:
        logger.error("訂單反查錯誤", extra={
            'order_id': order_id,
            'error': str(e)
        })
        typer.secho("訂單反查發生錯誤", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
