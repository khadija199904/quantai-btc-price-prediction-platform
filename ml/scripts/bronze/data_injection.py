import requests
import os
from dotenv import load_dotenv
import sys
import os
from pyspark.sql.functions import col, from_unixtime, to_timestamp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.scripts.spark_session import get_session  

load_dotenv() 
spark= get_session()
def data_collection():

  SYMBOL = 'BTCUSDT'
  INTERVAL = '1m'   # Intervalle d'une minute
  LIMIT = 600    
  api='https://api.binance.com/api/v3/klines'
  response = requests.get(api, params={
    "symbol": SYMBOL,
    "interval": INTERVAL,
    "limit": LIMIT
  })
  if response.status_code != 200:
        print(f"Erreur {response.status_code}")
        return None
  api_data=response.json()
  columns = [
        "open_time", "open_price", "high_price", "low_price", "close_price", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ]
  psdf= spark.createDataFrame(api_data, columns)
  
  num_cols= ["open_price", "high_price", "low_price", "close_price", "volume", "quote_asset_volume", "number_of_trades", "taker_buy_base_volume", "taker_buy_quote_volume"]
  for feature in num_cols:
      psdf= psdf.withColumn(feature, col(feature).cast('double'))

  psdf = psdf.withColumn("open_time_ts", to_timestamp(from_unixtime(col("open_time")/1000))) \
       .withColumn("close_time_ts", to_timestamp(from_unixtime(col("close_time")/1000)))
  
  
  psdf.write \
    .mode("append") \
    .parquet("data/bronze/binance_gold.parquet")
  return psdf

# data_collection()
