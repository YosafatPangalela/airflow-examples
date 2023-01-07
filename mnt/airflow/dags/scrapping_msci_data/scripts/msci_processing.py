from os.path import expanduser, join, abspath

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json

warehouse_location = abspath('spark-warehouse')

# Initialize Spark Session
spark = SparkSession \
    .builder \
    .appName("Msci processing") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()

# Read the file data_msci.json from the HDFS
df = spark.read.json('hdfs://namenode:9000/data/data_msci.json')

# Drop the duplicated rows based on the base and last_update columns
data_msci = df.select('code', 'security_name', 'price', 'shares', 'weight', 'currency', 'last_update') \
    .dropDuplicates(['code', 'last_update']) \
    .fillna(0)

# Export the dataframe into the Hive table data_msci
data_msci.write.mode("append").insertInto("data_msci")