'''
SparkSql文件入库
'''
from pyspark.sql import SQLContext
from pyspark.sql.types import *
# sc is an existing SparkContext.
sqlContext = SQLContext(sc)
# Load a text file and convert each line to a tuple.
lines = sc.textFile("auto.txt")
parts = lines.map(lambda l: l.split(","))
auto = parts.map(lambda p: (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
# The schema is encoded in a string.
schemaString = "EngSize Age Gender Marital exp Owner vAge Garage AntiTFD if_import Loss"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
# Apply the schema to the RDD.
schemaPeople = sqlContext.createDataFrame(auto, schema)
# Register the DataFrame as a table.
schemaPeople.registerTempTable("auto")
# SQL can be run over DataFrames that have been registered as a table.
results = sqlContext.sql("SELECT * FROM auto")

'''
ML__SparkSql文件入库
'''
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.mllib.linalg import Vectors
from pyspark.sql import Row,functions
from pyspark.ml.linalg import Vector,Vectors
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer,HashingTF, Tokenizer
from pyspark.ml.classification import LogisticRegression,LogisticRegressionModel, LogisticRegression


sqlContext = SQLContext(sc)
lines = sc.textFile("auto.txt")
parts = lines.map(lambda l: l.split(","))
auto = parts.map(lambda p:(Vectors.dense(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]),p[10]))
schema_auto = sqlContext.createDataFrame(auto, ["features","target"])
schema_auto.registerTempTable("auto_new")
data = sqlContext.sql("SELECT features,(case when target > 0 then 1 else 0 end)label FROM auto_new limit 50")

labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabel").fit(data)
featureIndexer = VectorIndexer().setInputCol("features").setOutputCol("indexedFeatures").fit(data)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

lr = LogisticRegression().setLabelCol("indexedLabel").setFeaturesCol("indexedFeatures").setMaxIter(10).setRegParam(0.3).setElasticNetParam(0.8)
print("LogisticRegression parameters:\n" + lr.explainParams())

labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(labelIndexer.labels)

lrPipeline =  Pipeline().setStages([labelIndexer, featureIndexer, lr, labelConverter])
lrPipelineModel = lrPipeline.fit(trainingData)

lrPredictions = lrPipelineModel.transform(testData)

preRel = lrPredictions.select("predictedLabel", "label", "features", "probability").collect()

for item in preRel:
    print(str(item['label'])+','+str(item['features'])+'-->prob='+str(item['probability'])+',predictedLabel'+str(item['predictedLabel']))
