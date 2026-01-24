import pytest
import pandas as pd
from pyspark.sql import SparkSession
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta  


from ml.scripts.silver.prepare_ml import prepare_ml_data
from ml.scripts.silver.clean_to_silver import clean_to_silver

@pytest.fixture(scope="session")
def spark():
    return (
        SparkSession.builder
        .appName("pytest-spark")
        .getOrCreate()
    )
  

# Exemple de dataframe fictive pour test
@pytest.fixture
def sample_data(spark):
    data = []
    data = []
    0
    base_time = datetime(2024, 1, 1, 10, 0, 0)
    for i in range(20):  
        data.append({
            "open_time_ts": base_time + timedelta(minutes=i),
            "open_price": 29000.0 + i,
            "high_price": 29500.0 + i,
            "low_price": 28900.0 + i,
            "close_price": 29400.0 + i,
            "volume": 1000.0,
            "taker_buy_base_volume": 600.0
        })
    return spark.createDataFrame(data)
# --------------- Test la fonction clean_to_silver ---------------------------------
def test_clean_to_silver(spark,sample_data):

    with patch("pyspark.sql.DataFrameReader.parquet") as mock_read:
        mock_read.return_value = sample_data

        assert sample_data.schema["open_time_ts"].dataType.simpleString() == "timestamp"

        df_result = clean_to_silver() 
        # Vérifier que les nouvelles colonnes existent
        expected_columns = ["returns", "MA_5", "MA_10", "taker_ratio", "target_close"]
        for col in expected_columns:
            assert col in df_result.columns
