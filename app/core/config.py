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

    # OnlinePay Settings
    CHARGE_APP_STATUS_URL: str = ""
    ONLINE_PAY_MERCHANT_KEY: str = ""
    ONLINE_PAY_CORPORATE_ID: str = ""
    ONLINE_PAY_AUTH_PAY: str = ""
    ONLINE_PAY_ENTRY_MODE: str = ""
    ONLINE_PAY_CORP_ID: str = ""
    GET_CTBC_OPW_PAYMENT_API_URL: str = ""

    # ICP Settings
    ICP_ENC_KEY_ID: str = ""
    ICP_TIMEOUT: int = 30
    ICP_API_BASE_URL: str = ""
    ICP_PLATFORM_ID: str = ""
    ICP_MERCHANT_ID: str = ""
    
    # ICP Crypto Settings
    ICP_CLIENT_PRIVATE_KEY_PATH: str = "storage/keys/icp_client_private.key"
    ICP_SERVER_PUBLIC_KEY_PATH: str = "storage/keys/icp_server_public.pem"
    ICP_AES_KEY: str = ""
    ICP_AES_IV: str = ""
    ICP_AES_MODE: str = "AES-128-CBC"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
