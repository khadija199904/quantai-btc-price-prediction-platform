from airflow.decorators import dag, task
import pendulum
from ml.scripts.bronze.data_injection import data_collection
from ml.scripts.spark_session import spark
from ml.scripts.silver.prepare_ml import prepare_ml_data
from ml.scripts.silver.training import train_evaluate_models
from ml.scripts.silver.clean_to_silver import clean_to_silver

@dag(
  schedule=None,
  start_date= pendulum.datetime(2026, 1, 20, tz="UTC"),
  catchup = False,
  tags=['crypto','btc']
  ) 

def btc_dag():
    
    @task
    def data_injection_task():
        
        df = data_collection(spark)  
        bronze_path = "data/bronze/binance_gold.parquet"
        df.write.mode("overwrite").parquet(bronze_path)
        return bronze_path
       
    @task
    def FE_Cleaning_task(bronze_path : str) :
        """
        Lit la zone Bronze, transforme les données et sauvegarde en zone Silver.
        """
        df_silver = clean_to_silver()
        path_silver = "data/silver/binance_silver.parquet"
        return path_silver

    @task
    def training_task(silver_path : str):
        
        
        df = spark.read.json(silver_path)

        # Préparation et entraînement
        train_data, test_data, assembler = prepare_ml_data(df)
        best_model = train_evaluate_models(train_data, test_data, assembler)
        return f"Meilleur modèle sauvegardé !"

    # Orchestration du flux (Pipeline)
    path_bronze = data_injection_task()
    path_silver = FE_Cleaning_task(path_bronze)
    training_task(path_silver)


btc_dag()

