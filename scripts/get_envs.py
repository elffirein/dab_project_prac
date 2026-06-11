import os
print(f"Callback Host: {os.environ.get('_PYSPARK_DRIVER_CALLBACK_HOST', 'Not Set')}")
print(f"Local IP: {os.environ.get('SPARK_LOCAL_IP', 'Not Set')}")
