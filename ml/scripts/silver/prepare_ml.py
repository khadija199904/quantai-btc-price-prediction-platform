from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler 

def prepare_ml_data(data, features_cols=None):
    """
    Prépare les données pour l'entraînement ML : création de l'index temporel et split train/test.
    """
    if features_cols is None:
        features_cols = ["returns", "MA_5", "MA_10", "taker_ratio"]

    assembler = VectorAssembler(inputCols=features_cols, outputCol="features", handleInvalid="skip")
    window = Window.orderBy("open_time_ts")
    df = data.withColumn("time_index", F.row_number().over(window))
    
    # Split séquentiel
    total_count = df.count()
    split_point = int(0.8 * total_count)
    
    train_data = df.filter(F.col("time_index") <= split_point)
    test_data = df.filter(F.col("time_index") > split_point)

    return train_data, test_data, assembler