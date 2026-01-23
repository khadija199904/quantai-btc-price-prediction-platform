import os
import sys

# Add parent directory to sys.path to import spark_session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler ,StandardScaler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from bronze.data_injection import data_collection
from silver.clean_to_silver import clean_to_silver

def training_evaluation_model(data):
 
    features_cols = ["returns", "MA_5", "MA_10", "taker_ratio"]
    
    target = "target_close"

    assembler = VectorAssembler(inputCols=features_cols, outputCol="features",handleInvalid="skip")
    window = Window.orderBy("open_time_ts")
    df = data.withColumn("time_index", F.row_number().over(window))

   
    # Séparation séquentielle
    total_count = df.count()
    split_point = int(0.8 * total_count)
    
    train_data = df.filter(F.col("time_index") <= split_point)
    test_data= df.filter(F.col("time_index") > split_point)
    
    # Transormations
    scaler = StandardScaler(inputCol="features", outputCol="features_scaled", withStd=True, withMean=True)

    models = [
        ("Linear Regression", LinearRegression(featuresCol="features_scaled", labelCol=target)),
        
        ("Random Forest", RandomForestRegressor(featuresCol="features_scaled", labelCol=target, numTrees=100, maxDepth=10, 
                       seed=42)),
        
       
    ]  
    #  Évaluateurs
    evaluator_r2 = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="r2")
    evaluator_mae = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="mae")
    evaluator_rmse = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="rmse")
    
    best_rmse = float("inf")
    best_model_name = None
    for model_name, model_algo in models:
        print(f"Entraînement du modèle : {model_name}...")
    
        # Créer pipeline
        pipeline = Pipeline(stages=[assembler, scaler, model_algo])

        # Entraîner modèle
        model_fit = pipeline.fit(train_data)
        # Prédiction
        preds = model_fit.transform(test_data)
        # Évaluation
        r2 = evaluator_r2.evaluate(preds)
        mae = evaluator_mae.evaluate(preds)
        rmse = evaluator_rmse.evaluate(preds)
        
        print(f"Modèle: {model_name}")

        print(f"R²: {r2:.4f} | MAE: {mae:.2f} | RMSE: {rmse:.2f}")
        
        if rmse < best_rmse:
            best_rmse = rmse
            best_model_fit = model_fit
            best_model_name = model_name


    if best_model_fit :
        save_path  = f"ml/saved_model/{best_model_name}_pipeline"
        model_fit.write().overwrite().save(save_path )
        print(f"\n MEILLEUR MODÈLE : {best_model_name} sauvegardé dans '{save_path}' avec un RMSE de {best_rmse:.2f}")
    
    return best_model_fit
data_collection()
data=clean_to_silver()
training_evaluation_model(data)