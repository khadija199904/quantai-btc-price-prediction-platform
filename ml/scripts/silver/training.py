
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import StandardScaler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor


def train_evaluate_models(train_data, test_data, assembler, target="close_t_plus_10"):
    scaler = StandardScaler(inputCol="features", outputCol="features_scaled", withStd=True, withMean=True)

    models = [
        ("Linear Regression", LinearRegression(featuresCol="features_scaled", labelCol=target)),
        ("Random Forest", RandomForestRegressor(featuresCol="features_scaled", labelCol=target, numTrees=100, maxDepth=10, seed=42)),
        ("Linear Regression ElasticNet", LinearRegression(featuresCol="features_scaled", labelCol=target, regParam=0.1, elasticNetParam=0.5))
    ]
    
    evaluator_r2 = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="r2")
    evaluator_mae = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="mae")
    evaluator_rmse = RegressionEvaluator(labelCol=target, predictionCol="prediction", metricName="rmse")
    
    best_rmse = float("inf")
    best_model_fit = None
    best_model_name = None
    
    for model_name, model_algo in models:
        print(f"Entraînement du modèle : {model_name}...")
        pipeline = Pipeline(stages=[assembler, scaler, model_algo])
        model_fit = pipeline.fit(train_data)
        preds = model_fit.transform(test_data)
        
        r2 = evaluator_r2.evaluate(preds)
        mae = evaluator_mae.evaluate(preds)
        rmse = evaluator_rmse.evaluate(preds)
        
        print(f"Modèle: {model_name} | R²: {r2:.4f} | MAE: {mae:.2f} | RMSE: {rmse:.2f}")
        
        if rmse < best_rmse:
            best_rmse = rmse
            best_model_fit = model_fit
            best_model_name = model_name

    if best_model_fit:
       
        save_path  = f"../saved_model/{best_model_name}_pipeline"
        best_model_fit.write().overwrite().save(save_path)
        print(f"\nMEILLEUR MODÈLE : {best_model_name} sauvegardé dans '{save_path}' avec RMSE {best_rmse:.2f}")
    
    return best_model_fit

if __name__ == "__main__":
   from prepare_ml import pprepare_ml_data
   train_data, test_data, assembler = prepare_ml_data(df_silver)