import pytest
import pandas as pd
from pyspark.sql import SparkSession

from ml.scripts.silver.prepare_ml import prepare_ml_data

@pytest.fixture(scope="session")
def spark():
    return (
        SparkSession.builder
        .master("local[1]")
        .appName("pytest-spark")
        .getOrCreate()
    )

# Exemple de dataframe fictive pour test
@pytest.fixture
def sample_data(spark):
    data = [
    {
        "open_time": 1609459200000,
        "open_price": 29000.0,
        "high_price": 29500.0,
        "low_price": 28900.0,
        "close_price": 29400.0,
        "volume": 1000.0,
        "close_time": 1609462800000,
        "quote_asset_volume": 5000000.0,
        "number_of_trades": 1200,
        "taker_buy_base_volume": 600.0,
        "taker_buy_quote_volume": 3000000.0,
        "ignore": 0,
        "open_time_ts": 1609459200,
        "close_time_ts": 1609462800
    },
    {
        "open_time": 1609462800000,
        "open_price": 29400.0,
        "high_price": 29600.0,
        "low_price": 29100.0,
        "close_price": 29200.0,
        "volume": 1100.0,
        "close_time": 1609466399999,
        "quote_asset_volume": 5100000.0,
        "number_of_trades": 1300,
        "taker_buy_base_volume": 650.0,
        "taker_buy_quote_volume": 2350000.0,
        "ignore": 0,
        "open_time_ts": 1609462800,
        "close_time_ts": 1609466399
    }
   ]

    df = spark.createDataFrame(data)
    return df 

# Test de la fonction de préparation des données
def test_prepare_data(sample_data):
    cols = ["target_close", "returns", "MA_5", "MA_10","taker_ratio"]
    
    train_df, test_df, assembler = prepare_ml_data(sample_data)

    # Vérifie que les DataFrames ne sont pas vides
    assert train_df.count() > 0
    assert test_df.count() >= 0

    # Vérifie que la colonne 'time_index' a été créée
    assert "time_index" in train_df.columns
    assert "time_index" in test_df.columns

    # Vérifie que l'assembleur contient bien les colonnes attendues
    expected_features = ["returns", "MA_5", "MA_10", "taker_ratio"]
    assert assembler.getInputCols() == expected_features
    assert assembler.getOutputCol() == "features"