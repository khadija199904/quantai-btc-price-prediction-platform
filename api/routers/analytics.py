from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.dependencies import get_db, get_current_user
from api.schemas.analytics import AnalyticsResponse, MarketSummary, PriceTrend, VolumeStats
from api.crud import analytics as crud_analytics
import logging

logger = logging.getLogger("quantai-api")
router = APIRouter()

@router.get("/summary", response_model=MarketSummary)
def read_market_summary(db: Session = Depends(get_db)):
    summary = crud_analytics.get_market_summary(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No market data available")
    return summary

@router.get("/trends", response_model=List[PriceTrend])
def read_price_trends(limit: int = 100, db: Session = Depends(get_db)):
    return crud_analytics.get_price_trends(db, limit=limit)

@router.get("/volume", response_model=VolumeStats)
def read_volume_metrics(hours: int = 24, db: Session = Depends(get_db)):
    return crud_analytics.get_volume_metrics(db, hours=hours)

@router.get("/full", response_model=AnalyticsResponse)
def read_full_analytics(db: Session = Depends(get_db)):
    summary = crud_analytics.get_market_summary(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No market data available")
    
    trends = crud_analytics.get_price_trends(db, limit=100)
    volume_metrics = crud_analytics.get_volume_metrics(db, hours=24)
    
    return {
        "summary": summary,
        "trends": trends,
        "volume_metrics": volume_metrics
    }
