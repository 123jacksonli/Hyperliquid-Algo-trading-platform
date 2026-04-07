"""本地 API：供 Next.js 或腳本呼叫，與 Hyperliquid 唯讀資料橋接。

啟動：在 `python/` 下且已啟用 venv 後執行
  uvicorn system_arti.api.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from system_arti import __version__
from system_arti.config import get_settings
from system_arti.hl import HyperliquidService

app = FastAPI(
    title="System-Arti Trading API",
    version=__version__,
    description="Hyperliquid 演算法交易後端（唯讀 + 健康檢查）。",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "system-arti-python"}


@app.get("/api/v1/status")
def api_status() -> dict[str, Any]:
    settings = get_settings()
    hl = HyperliquidService()
    snap = hl.market_snapshot()
    user = hl.user_readonly_summary(settings.wallet_address)
    return {
        "version": __version__,
        "hyperliquid": snap,
        "user": user,
        "wallet_configured": bool(settings.wallet_address),
    }
