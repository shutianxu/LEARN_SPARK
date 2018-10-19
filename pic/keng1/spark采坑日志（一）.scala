spark采坑日志（一）

北极星指标
  val polestarDataFrame = polestar.polestarData()
  logger.warn("polestarDataFrame making finished.")
  polestarDataFrame.repartition('idvisit).write.mode("overwrite").parquet(s"${ Settings.destination }/polestar")
  logger.warn("polestarDataFrame loading finished.")
通过repartition来做分区，分担每个节点存储

本地测试通过，集群上测试挂掉：

<img src="/Users/2mofang/Documents/spark_/SPARK/pic/1539832170681.jpg">

集群的Executors过载导致错误，处理2.5亿的数据量时报错（JOIN，窗口等）
执行--executor-memory 10G
如下：
- spark-submit --master yarn --deploy-mode cluster --executor-memory 10G --class com.mofang.insightdiscovery.DataProcess build/libs/InsightDiscovery-*-all.jar
executor()
执行未报错，但是写文件报错，分配了5个executor(SPARK自动分配?)，均为5.5G，未达到10G？

通过查看SPARKUI，内存消耗超过了22.2G，所以有两种方法处理：
<img src="/Users/2mofang/Documents/spark_/SPARK/pic/1539832959103.jpg">

1.扩容：33G -> 100G
2.改为增量写入文件，牺牲时间

