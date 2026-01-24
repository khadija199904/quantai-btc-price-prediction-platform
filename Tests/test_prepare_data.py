import pytest
import pandas as pd
from pyspark.sql import SparkSession
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta  


from ml.scripts.silver.prepare_ml import prepare_ml_data
from ml.scripts.silver.clean_to_silver import clean_to_silver

@pytest.fixture(scope="function")
def spark():
    return (
        SparkSession.builder
        .appName("pytest-spark")
        .getOrCreate()
    )
  

# Exemple de dataframe fictive pour test
@pytest.fixture
def silver_data(spark):
    data = []
    data = []
    0
    base_time = datetime(2024, 1, 1, 10, 0, 0)
    for i in range(20):  
        data.append({
            "open_time_ts": base_time + timedelta(minutes=i),
            "open_price": 45000.0 + i,
            "high_price": 55500.0 + i,
            "low_price": 30900.0 + i,
            "close_price": 45400.0 + i,
            "volume": 2000.0,
            "taker_buy_base_volume": 1200.0
        })
    return spark.createDataFrame(data)

# --------------- Test la fonction prepare_ml_data ---------------------------------


def test_prepare_ml_data_assembler(spark, silver_data):
    
    
    features = ["TeamBTCPrijet","Khadija", "Maryem","Said","TalAIt","SimplonMaghreb"]
    _, _, assembler = prepare_ml_data(silver_data, features_cols=features)

    # Vérifie que les colonnes d'entrée de l'assembler sont les bonnes
    assert assembler.getInputCols() == features
    assert assembler.getOutputCol() == "features"
    assert assembler.getHandleInvalid() == "skip"

def test_prepare_ml_data_columns(spark, silver_data):
    train_df, test_df, _ = prepare_ml_data(silver_data)
    
    assert "time_index" in train_df.columns

    # Respect de l'ordre (Le premier doit être l'index 1)
    first_row = train_df.orderBy("open_time_ts").first()
    assert first_row["time_index"] == 1, "Le time_index devrait commencer à 1 pour la donnée la plus ancienne"

    total_original = silver_data.count()
    assert train_df.count() + test_df.count() == total_original, "Le split ne doit pas perdre de lignes"

    


