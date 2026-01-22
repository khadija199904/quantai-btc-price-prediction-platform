from airflow.decorators import dag, task
import pendulum
from ml.scripts.bronze.data_injection import data_collection
@dag(
  schedule=None,
  start_date= pendulum.datetime(2026, 1, 20, tz="UTC")) 
def btc_dag():
    @task
    def data_injection_task():
         df= data_collection()
         json_data = df.toJSON().collect()
         return json_data
    
    data_injection_task()
btc_dag()