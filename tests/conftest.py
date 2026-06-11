import os
import sys
import pytest

# Adjust the sys.path to include the src directory
sys.path.append(os.getcwd())

def pytest_configure(config):
    """Runs before any tests or fixtures are even loaded."""
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
    os.environ["_PYSPARK_DRIVER_CALLBACK_HOST"] = "127.0.0.1"
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    # This prevents Spark from picking up the Docker hostname during early init
    os.environ["SPARK_PUBLIC_DNS"] = "127.0.0.1"

@pytest.fixture()
def spark():
    print("Strting fixture")
    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.remote(cluster_id="0608-230939-89meszhe").getOrCreate()
        print("Using DatabricksSession")
    except ImportError:
        try:
            from pyspark.sql import SparkSession
            # 1. Force the callback host to localhost
            # os.environ["_PYSPARK_DRIVER_CALLBACK_HOST"] = "127.0.0.1"
            # os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

            # # 2. Ensure Spark uses the Python binary from your venv
            # os.environ["PYSPARK_PYTHON"] = sys.executable
            # os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

            #Print the environmnent variables to verify they are set correctly
            print(os.environ.get("_PYSPARK_DRIVER_CALLBACK_HOST", "Not Set"))
            print(os.environ.get("SPARK_LOCAL_IP", "Not Set"))
            print(os.environ.get("PYSPARK_PYTHON", "Not Set"))
            print(os.environ.get("PYSPARK_DRIVER_PYTHON", "Not Set"))

            spark = (SparkSession.builder
                                 .master("local[*]")
                                 # These two lines are critical to stop it from using 'host.docker.internal'
                                 .config("spark.driver.host", "127.0.0.1")
                                 .config("spark.driver.bindAddress", "127.0.0.1")
                                # This helps the worker find the driver
                                 .config("spark.python.worker.reuse", "true")
                                 .getOrCreate())
            #print("Using regular SparkSession")
            print("Spark Host: " + spark.sparkContext.getConf().get("spark.driver.host"))
            spark.range(10).collect() 
            print("Success!")
        except Exception as e:
            print(f"Error creating SparkSession: {e}")
            raise e
    #return spark
    yield spark
    spark.stop()
