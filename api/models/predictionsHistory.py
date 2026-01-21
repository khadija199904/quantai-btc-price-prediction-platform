
# from sqlalchemy import Column,Integer,String ,DateTime,ForeignKey,func ,Float
# from sqlalchemy.orm import relationship
# from api.database import Base


# # Table des logs d'analyses
# class PredictionHistory(Base):
#     __tablename__ = "predictions_history"

#     id = Column(Integer, primary_key=True)
#     timestamp = Column(DateTime, default=func.now(), nullable=False)
#     userid = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    
#     # predictions = Column(Float, nullable=False)

#     user = relationship("USERS", back_populates="predictions")