"""策略介面：之後實作具體策略時繼承 `Strategy`。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


class ExchangeAdapter(Protocol):
    """未來下單／查詢適配器；先以 Protocol 描述依賴，避免循環引用。"""

    def name(self) -> str: ...


@dataclass
class StrategyContext:
    symbol: str
    params: dict[str, Any]


class Strategy(ABC):
    """演算法策略基底類別。"""

    name: str = "unnamed"

    @abstractmethod
    def on_bar(self, ctx: StrategyContext, ohlcv: dict[str, Any]) -> dict[str, Any] | None:
        """收到新 K 線時呼叫；可回傳訊號或 None。"""
        raise NotImplementedError
