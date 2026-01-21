from pydantic import BaseModel,Field

    
class PredictionResponse(BaseModel):
    prediction_value: float
