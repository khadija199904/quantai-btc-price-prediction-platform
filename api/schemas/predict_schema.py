from pydantic import BaseModel,Field

    
class PredictionResponse(BaseModel):
    prediction: float
