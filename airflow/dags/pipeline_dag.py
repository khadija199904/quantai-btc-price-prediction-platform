from airflow.decorators import dag, task
import pendulum
from ml.scripts.bronze.data_injection import data_collection
from ml.scripts.spark_session import spark
from ml.scripts.silver.prepare_ml import prepare_ml_data
from ml.scripts.silver.training import train_evaluate_models

@dag(
  schedule=None,
  start_date= pendulum.datetime(2026, 1, 20, tz="UTC")) 
def btc_dag():
    
    @task
    def data_injection_task():
        
        df = data_collection(spark)  # 
        
        json_data = df.toJSON().collect()
        return json_data

    @task
    def training_task(json_data):
        
        rdd = spark.sparkContext.parallelize(json_data)
        df = spark.read.json(rdd)

        # Préparation et entraînement
        train_data, test_data, assembler = prepare_ml_data(df)
        best_model = train_evaluate_models(train_data, test_data, assembler)
        return f"Meilleur modèle sauvegardé !"

    # Orchestration
    json_data = data_injection_task()
    training_task(json_data)


btc_dag()

