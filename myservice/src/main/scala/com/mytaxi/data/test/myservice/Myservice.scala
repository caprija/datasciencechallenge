package com.mytaxi.data.test.myservice

import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.SparkSession

object Myservice extends App with LazyLogging {
  logger.info("starting myservice...")
  // TODO: You can either use this Scala project to start coding spark or create a new project in the language of your choice

  val spark = SparkSession.builder().appName("myservice").master("local[*]").getOrCreate()
  val hadoopConfig = spark.sparkContext.hadoopConfiguration
  hadoopConfig.set("fs.hdfs.impl", classOf[org.apache.hadoop.hdfs.DistributedFileSystem].getName)
  hadoopConfig.set("fs.file.impl", classOf[org.apache.hadoop.fs.LocalFileSystem].getName)

  spark.sql("select 1").show()

}
