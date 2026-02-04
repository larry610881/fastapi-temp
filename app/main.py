"""
FastAPI 應用程式入口點

整合 CORS、路由與全域錯誤處理
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 設定 - 根據環境動態調整
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 全域錯誤處理
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全域錯誤處理
    
    攔截所有未處理的 API 錯誤，確保：
    1. 錯誤被記錄
    2. 回傳統一的錯誤格式
    3. 不會洩漏內部錯誤細節（正式環境）
    """
    logger.error("未處理的 API 錯誤", extra={
        'path': request.url.path,
        'method': request.method,
        'error': str(exc),
        'error_type': type(exc).__name__
    })
    
    # 正式環境不顯示詳細錯誤
    error_message = str(exc) if not settings.is_production else "伺服器內部錯誤"
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": error_message,
            "error_type": type(exc).__name__ if not settings.is_production else None
        }
    )


# ==========================================
# 路由註冊
# ==========================================

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
