from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("btc_price_prediction").getOrder()
