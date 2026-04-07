from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """執行時設定（由環境變數或 .env 載入）。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    hl_api_url: str | None = Field(
        default=None,
        description="Hyperliquid HTTP API；預設使用 SDK 內建主網 URL。",
    )
    hl_testnet: bool = Field(default=False, description="是否使用測試網（若與 SDK 常數對應）。")

    wallet_address: str | None = Field(
        default=None,
        description="唯讀查詢用地址；私鑰請勿放此欄位。",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
