"""
CLI 入口點

使用 Typer 提供命令行介面，整合 DI Container 與全域錯誤處理
"""
import sys
import logging
import typer

from app.core.container import Container
from app.commands.charge_status import charge_status

logger = logging.getLogger(__name__)

# 初始化 DI Container
container = Container()
container.wire(modules=["app.commands.charge_status"])

app = typer.Typer()
app.command(name="charge-status")(charge_status)


def cli_exception_handler():
    """
    CLI 全域錯誤處理
    
    攔截所有未處理的 CLI 錯誤，確保：
    1. 錯誤被記錄
    2. 顯示使用者友善的錯誤訊息
    3. 程式以錯誤碼結束
    """
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n操作已取消")
        raise SystemExit(0)
    except Exception as e:
        logger.error("未處理的 CLI 錯誤", extra={
            'error': str(e),
            'error_type': type(e).__name__
        })
        typer.secho(f"發生未預期錯誤: {e}", fg=typer.colors.RED)
        typer.secho(f"錯誤類型: {type(e).__name__}", fg=typer.colors.YELLOW)
        raise SystemExit(1)


if __name__ == "__main__":
    cli_exception_handler()
