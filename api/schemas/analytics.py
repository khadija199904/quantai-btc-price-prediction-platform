from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PriceTrend(BaseModel):
    timestamp: datetime
    close_price: float

class VolumeStats(BaseModel):
    total_volume: float
    avg_volume: float
    max_volume: float

class MarketSummary(BaseModel):
    symbol: str = "BTCUSDT"
    current_price: float
    price_change_24h: float
    price_change_percent: float
    volume_24h: float
    last_update: datetime

class AnalyticsResponse(BaseModel):
    summary: MarketSummary
    trends: List[PriceTrend]
    volume_metrics: VolumeStats
