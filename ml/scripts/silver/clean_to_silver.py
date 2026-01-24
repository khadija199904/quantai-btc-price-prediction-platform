import os
import sys
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Add parent directory to sys.path to import spark_session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spark_session import spark
def clean_to_silver():
    print("Spark context initialized.")
    print("Reading data from Bronze zone...")
    bronze_path = "data/bronze/binance_gold.parquet"
    
    if not os.path.exists(bronze_path):
        print(f"Error: Bronze data not found at {bronze_path}")
        return

    # Load Bronze data
    df = spark.read.parquet(bronze_path)
    print(f"Schema: {df.schema}")
    print(f"Bronze count: {df.count()}")
    
    # Define window for time-series operations
    # Data is already chronologically ordered in Binance API, but we order by open_time_ts just in case
    window_spec = Window.orderBy("open_time_ts")
    
    print("Calculating target and features...")
    
    # 1. Target: Price 10 minutes (10 rows) in the future
    df = df.withColumn("target_close", F.lead("close_price", 10).over(window_spec))
    print("Target added.")
    
    # 2. Return: Variation relative to the previous minute
    df = df.withColumn("returns", (F.col("close_price") / F.lag("close_price", 1).over(window_spec)) - 1)
    print("Returns added.")
    
    # 3. Moving Averages (5 and 10 minutes)
    window_ma5 = Window.orderBy("open_time_ts").rowsBetween(-5, -1)
    window_ma10 = Window.orderBy("open_time_ts").rowsBetween(-10, -1)
    
    df = df.withColumn("MA_5", F.avg("close_price").over(window_ma5))
    df = df.withColumn("MA_10", F.avg("close_price").over(window_ma10))
    print("MAs added.")
    
    # 4. Taker Ratio
    df = df.withColumn("taker_ratio", F.col("taker_buy_base_volume") / F.col("volume"))
    print("Taker ratio added.")

    # Features temporelles
    df = df.withColumn("hour", F.hour(F.col("open_time_ts")))
    df = df.withColumn("day_of_week", F.dayofweek(F.col("open_time_ts")))
    df = df.withColumn("minute", F.minute(F.col("open_time_ts")))
    
    print("Cleaning data...")
    print(f"Current columns: {df.columns}")
    
    # Remove rows where target is null (last 10 rows)
    df_cleaned = df.dropna(subset=["target_close", "returns", "MA_5", "MA_10","taker_ratio"])
    print("Nulls dropped.")
    
    # Select final columns for Silver Zone
    # we keep original prices and volume for reference, plus new features and target
    silver_columns = [
        "open_time_ts", "open_price", "high_price", "low_price", "close_price", "volume",
        "returns", "MA_5", "MA_10", "taker_ratio", "target_close"
    ]
    df_silver = df_cleaned.select(*silver_columns)
    
    print(f"Silver DataFrame count: {df_silver.count()}")
    
    # Save to Silver zone (Parquet)
    silver_path = "data/silver/binance_silver.parquet"
    print(f"Saving to Silver zone: {silver_path}")
    df_silver.write.mode("overwrite").parquet(silver_path)

    # Save to PostgreSQL
    print("Exporting to PostgreSQL...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = f"jdbc:postgresql://{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'postgres')}"
        db_properties = {
            "user": os.getenv('DB_USER', 'postgres'),
            "password": os.getenv('DB_PASSWORD', 'postgres'),
            "driver": "org.postgresql.Driver"
        }
        
        df_silver.write.jdbc(
            url=db_url,
            table=os.getenv('DB_TABLE', 'btc_silver'),
            mode="overwrite",
            properties=db_properties
        )
        print("Export to PostgreSQL complete!")
    except Exception as e:
        print(f"PostgreSQL export failed: {e}")
        print("Note: Ensure PostgreSQL is running and credentials in .env are correct.")
    
    print("Transformation complete!")
    spark.stop()

    return df_silver

if __name__ == "__main__":
    try:
        clean_to_silver()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
