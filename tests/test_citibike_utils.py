# test_citibike_utils.py
import datetime
from src.citibike.citibike_utils import get_trip_duration_mins
from pyspark.sql import SparkSession


# Adjust the sys.path if needed (usually in conftest.py or at the top of your test files)

def test_get_trip_duration_mins(spark):

    # create a spark session
    # Ensure PySpark uses the current Python interpreter and binds the driver to
    # localhost so Python workers can connect back reliably on Windows.
    # import os
    # # Set the callback host to localhost
    # os.environ["_PYSPARK_DRIVER_CALLBACK_HOST"] = "127.0.0.1"
    # os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
    # os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    # os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

    # spark = (
    #     SparkSession.builder
    #     .master("local[*]")
    #     .appName("test_get_trip_duration_mins")
    #     .config("spark.driver.host", "127.0.0.1")
    #     .config("spark.driver.bindAddress", "127.0.0.1")
    #      .config("spark.network.timeout", "300s")
    #     .getOrCreate()
    # )
            
    # Create a test DataFrame with known start and end timestamps using datetime objects
    data = [
        (datetime.datetime(2025, 4, 10, 10, 0, 0), datetime.datetime(2025, 4, 10, 10, 10, 0)),  # 10 minutes
        (datetime.datetime(2025, 4, 10, 10, 0, 0), datetime.datetime(2025, 4, 10, 10, 30, 0))   # 30 minutes
    ]
    
    # Apply the function to calculate trip duration in minutes
    schema = "start_time timestamp, end_time timestamp"
    df = spark.createDataFrame(data, schema=schema)
    result_df = get_trip_duration_mins(spark, df, "start_time", "end_time", "trip_duration_mins")
    
    
    # Collect the results for assertions
    results = result_df.select("trip_duration_mins").collect()
    
    # Assert that the differences are as expected
    assert results[0]["trip_duration_mins"] == 10
    assert results[1]["trip_duration_mins"] == 30
    