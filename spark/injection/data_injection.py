import requests
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.spark_session import spark

load_dotenv() 
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
  psdf.write \
    .mode("overwrite") \
    .parquet("data/bronze/binance_gold.parquet")
  return psdf
data_collection()
