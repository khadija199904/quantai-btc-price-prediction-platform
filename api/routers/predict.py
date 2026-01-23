from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from api.dependencies import get_db,get_current_user
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from api.models.users import USERS
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import desc
import sys
from pathlib import Path
from pyspark.ml import PipelineModel
router = APIRouter()
spark= SparkSession.builder.appName("initialize_spark").getOrCreate()

#db: Session = Depends(get_db),current_user: USERS = Depends(get_current_user) 
@router.post("/predict")
async def make_prediction():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    model_path = PROJECT_ROOT / "ml" / "saved_model" / "Linear Regression_pipeline"
    try:
        model = PipelineModel.load(str(model_path))
        silver_path = "data/silver/binance_silver.parquet"
        df= spark.read.parquet(silver_path)
        data= df.orderBy(desc('open_time_ts')).limit(1)
        #prediction= model.predict(data)
        print(data)
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}