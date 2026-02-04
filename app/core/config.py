from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Hybrid Boilerplate"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "DEV_SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520 # 8 days

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment Settings
    # 環境設定: local, staging, production
    ENVIRONMENT: str = "local"
    
    # Initialization Toggle
    # 是否允許資料庫初始化 (為了安全，預設為 False)
    # 必須顯式設定環境變數 INIT_DB=True 才會執行初始化腳本
    INIT_DB: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
