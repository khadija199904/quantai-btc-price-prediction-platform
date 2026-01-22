import os
import sys
from pyspark.sql import SparkSession

# Set environment variables for Spark on Windows
# Assuming project structure: project_root/ml/scripts/spark_session.py
# and project_root/hadoop/bin/winutils.exe
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HADOOP_DIR = os.path.join(PROJECT_ROOT, 'hadoop')

os.environ['HADOOP_HOME'] = HADOOP_DIR
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PATH'] = os.path.join(HADOOP_DIR, 'bin') + os.pathsep + os.environ.get('PATH', '')

spark = SparkSession.builder \
    .appName("btc_price_prediction") \
    .config(
        "spark.jars.packages",
        "org.postgresql:postgresql:42.7.3"
    ) \
    .getOrCreate()


