"""Hyperliquid 連線與唯讀查詢的薄包裝，集中 SDK 使用點便於測試與替換。"""

from __future__ import annotations

from typing import Any

from hyperliquid.info import Info

from system_arti.config import get_settings


class HyperliquidService:
    def __init__(self, *, skip_ws: bool = True) -> None:
        settings = get_settings()
        base = settings.hl_api_url
        self._info = Info(base_url=base, skip_ws=skip_ws)

    @property
    def info(self) -> Info:
        return self._info

    def market_snapshot(self) -> dict[str, Any]:
        """回傳可公開取得的市場摘要（不需私鑰）。"""
        meta = self._info.meta()
        mids = self._info.all_mids()
        universe = meta.get("universe") or []
        names = [u.get("name") for u in universe if u.get("name")]
        sample = names[:12]
        return {
            "perp_markets": len(universe),
            "sample_symbols": sample,
            "mids_count": len(mids) if isinstance(mids, dict) else 0,
        }

    def user_readonly_summary(self, address: str | None) -> dict[str, Any] | None:
        """若提供地址則回傳使用者狀態摘要；否則為 None。"""
        if not address:
            return None
        state = self._info.user_state(address)
        if not isinstance(state, dict):
            return {"raw_type": type(state).__name__}
        margin = state.get("marginSummary") or state.get("crossMarginSummary") or {}
        return {
            "account_value": margin.get("accountValue"),
            "withdrawable": margin.get("totalRawUsd"),
        }
