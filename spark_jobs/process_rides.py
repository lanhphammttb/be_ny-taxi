from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RidesETL").getOrCreate()
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://db:5432/ny_taxi") \
    .option("dbtable", "rides") \
    .option("user", "postgres") \
    .option("password", "Khongbiet098") \
    .load()

# ETL Logic: Ví dụ filter rides completed
df.filter("ride_status = 'completed'").show()
