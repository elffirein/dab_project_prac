from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.remote(cluster_id="0608-230939-89meszhe").getOrCreate()
spark.sql("select 1").show()
