"""
資料庫連線設定

統一管理 SQLAlchemy Async Engine 與 Session
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 建立非同步引擎，配置連線池參數
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,         # 連線使用前檢查有效性
    pool_size=5,                # 連線池大小
    max_overflow=10,            # 額外允許的連線數
    pool_timeout=30,            # 等待連線的超時秒數
    pool_recycle=1800,          # 連線回收時間（30分鐘）
)

# Session 工廠
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """提供 DB Session 的依賴注入 (FastAPI 用)"""
    async with SessionLocal() as session:
        yield session
