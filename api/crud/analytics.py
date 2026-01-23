from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.btc_silver import BTCSilver
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("quantai-api")

def get_market_summary(db: Session):
    try:
        # Get the latest row
        latest = db.query(BTCSilver).order_by(BTCSilver.open_time_ts.desc()).first()
        if not latest:
            return None

        # Calculate 24h change (approximated as last 1440 mins)
        day_ago_ts = latest.open_time_ts - timedelta(days=1)
        day_ago_record = db.query(BTCSilver).filter(BTCSilver.open_time_ts >= day_ago_ts).order_by(BTCSilver.open_time_ts.asc()).first()
        
        price_change = 0
        price_change_pct = 0
        if day_ago_record:
            price_change = latest.close_price - day_ago_record.close_price
            price_change_pct = (price_change / day_ago_record.close_price) * 100

        # Calculate 24h total volume
        vol_24h = db.query(func.sum(BTCSilver.volume)).filter(BTCSilver.open_time_ts >= day_ago_ts).scalar() or 0

        return {
            "symbol": "BTCUSDT",
            "current_price": latest.close_price,
            "price_change_24h": price_change,
            "price_change_percent": price_change_pct,
            "volume_24h": vol_24h,
            "last_update": latest.open_time_ts
        }
    except Exception as e:
        logger.error(f"Error fetching market summary: {e}")
        raise

def get_price_trends(db: Session, limit: int = 100):
    try:
        records = db.query(BTCSilver).order_by(BTCSilver.open_time_ts.desc()).limit(limit).all()
        # Return in ascending order for charting
        return [{"timestamp": r.open_time_ts, "close_price": r.close_price} for r in reversed(records)]
    except Exception as e:
        logger.error(f"Error fetching price trends: {e}")
        raise

def get_volume_metrics(db: Session, hours: int = 24):
    try:
        since = datetime.now() - timedelta(hours=hours)
        stats = db.query(
            func.sum(BTCSilver.volume).label("total"),
            func.avg(BTCSilver.volume).label("avg"),
            func.max(BTCSilver.volume).label("max")
        ).filter(BTCSilver.open_time_ts >= since).one()
        
        return {
            "total_volume": stats.total or 0,
            "avg_volume": stats.avg or 0,
            "max_volume": stats.max or 0
        }
    except Exception as e:
        logger.error(f"Error fetching volume metrics: {e}")
        raise
