from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("btc_price_prediction") \
    .config(
        "spark.jars.packages",
        "org.postgresql:postgresql:42.7.3"
    ) \
    .getOrCreate()


