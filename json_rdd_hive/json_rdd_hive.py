from pyspark.sql import HiveContext

# sc is an existing SparkContext.
sqlContext = HiveContext(sc)

# A JSON dataset is pointed to by path.
# The path can be either a single text file or a directory storing text files.

shiguang = sqlContext.read.json("/user/1707500/shiguangwang.json")

# root
#  |-- age: integer (nullable = true)
#  |-- name: string (nullable = true)
shiguang.printSchema()

# Register this DataFrame as a table.
shiguang.registerTempTable("shiguangwang")

# SQL statements can be run by using the sql methods provided by `sqlContext`.
sqlContext.sql("use sparktest")
teenager = sqlContext.sql("CREATE TABLE shiguang asSELECT * FROM shiguangwang")

