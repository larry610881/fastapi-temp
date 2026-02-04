"""
應用程式設定

使用 Pydantic Settings 管理環境變數與設定
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional, List


class Settings(BaseSettings):
    PROJECT_NAME: str = "PayChecked Admin"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "DEV_SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment Settings
    # 環境設定: local, staging, production
    ENVIRONMENT: str = "local"
    
    # CORS Origins (逗號分隔)
    CORS_ORIGINS: str = "*"
    
    # Initialization Toggle
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

    @field_validator('ENVIRONMENT')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ['local', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'ENVIRONMENT must be one of {allowed}')
        return v

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v:
            raise ValueError('DATABASE_URL is required')
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """取得 CORS Origins 列表"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def is_production(self) -> bool:
        """是否為正式環境"""
        return self.ENVIRONMENT == "production"


settings = Settings()
