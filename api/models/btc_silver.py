from sqlalchemy import Column, Float, DateTime, BigInteger
from api.database import Base

class BTCSilver(Base):
    __tablename__ = "btc_silver"

    # Spark's JDBC write doesn't create a PK by default, 
    # but SQLAlchemy requires one. open_time_ts is unique.
    open_time_ts = Column(DateTime, primary_key=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    returns = Column(Float)
    MA_5 = Column(Float)
    MA_10 = Column(Float)
    taker_ratio = Column(Float)
    target_close = Column(Float)
