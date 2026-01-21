from sqlalchemy import Column,Integer,String ,DateTime,func
from sqlalchemy.orm import relationship
from api.database import Base



class USERS(Base) :
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password_hash = Column(String, nullable=False)
    createdat = Column(DateTime,default=func.now())

    
    # predictions = relationship("PredictionHistory", back_populates="user")
