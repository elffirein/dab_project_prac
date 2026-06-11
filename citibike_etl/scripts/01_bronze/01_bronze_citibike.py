from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType
from pyspark.sql.functions import create_map, lit
import sys

pipeline_id = sys.argv[1]
run_id = sys.argv[2]
task_id = sys.argv[3]
processed_timestamp = sys.argv[4]
catalog = sys.argv[5]

# Define the schema for the Citibike data
citibike_schema = StructType([
    StructField("ride_id", StringType(), True),
    StructField("rideable_type", StringType(), True),
    StructField("started_at", TimestampType(), True),
    StructField("ended_at", TimestampType(), True),
    StructField("start_station_name", StringType(), True),
    StructField("start_station_id", StringType(), True),
    StructField("end_station_name", StringType(), True),
    StructField("end_station_id", StringType(), True),
    StructField("start_lat", StringType(), True),
    StructField("start_lng", StringType(), True),
    StructField("end_lat", StringType(), True),
    StructField("end_lng", StringType(), True),
    StructField("member_casual", StringType(), True)
])

df = (spark.read.format("csv")
                .option("header", "true")
                .schema(citibike_schema)
                .load(f"/Volumes/{catalog}/00_landing/source_citibike_data/JC-202503-citibike-tripdata.csv")
)

df = df.withColumn("metadata",
                    create_map(
                        lit("pipeline_id"), lit(pipeline_id),
                        lit("run_id"), lit(run_id),
                        lit("task_id"), lit(task_id),
                        lit("processed_date"), lit(processed_timestamp)
                    )
)

write_query = (df.write
                 .mode("overwrite")
                 .option("mergeSchema", "true")
                 .saveAsTable(f"{catalog}.01_bronze.jc_citibike")
)



