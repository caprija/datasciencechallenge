import os
from pyspark.sql import functions as F
from mytaxi.etl_driver import ETLDriver
from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext
from pandas.testing import assert_frame_equal



def test_capitalize_column_value():
    etl_driver = ETLDriver()
    conf = SparkConf().setMaster("local[*]").setAppName("testservice")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    input_df = sqlContext.createDataFrame([(1, "china"),(2, "brazil"),(3, "germany"),], ["id", "country"])
    output_df = etl_driver.capitalize_column_value(input_df, "country")
    expected_df =  sqlContext.createDataFrame([(1, "China"),(2, "Brazil"),(3, "Germany"),], ["id", "country"])
    assert_frame_equal(expected_df.toPandas(), output_df.toPandas())




if __name__ == '__main__':

    test_capitalize_column_value()