import sys
import os
import json
import time
import logging
from etl_driver import ETLDriver
os.environ["PYSPARK_PYTHON"]='/usr/bin/python3'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0 pyspark-shell'
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession, Row, DataFrame, SQLContext, Window
from pyspark.sql import functions as F
from pyspark.sql.functions import *

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

class KafkaConsumer(object):
    """
    This class serves as to consume the user events from kafka and print them to the log.
    It cleans the data by conforming them in standard format like  capitalize country column, convert date in standard format
    Calculate some measures like unique users, most and least represented country
    """

    def __init__(self):
        self.etl_driver = ETLDriver()
        logging.basicConfig(level=logging.INFO)
        logging.info('Call MyService')

    def getSqlContextInstance(self, sparkContext):
        if ('sqlContextSingletonInstance' not in globals()):
            globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
        return globals()['sqlContextSingletonInstance']

    def process_user_events(self):
        """
        It create the spark connection with kafka stream and get user events after every 1 minute
        After recieving event, it Print all payments on log
        :return: None
        :rtype: NOne
        """
        try:
            conf = SparkConf().setMaster("local[*]").setAppName("consumerservice")
            sc = SparkContext(conf=conf)

            ssc = StreamingContext(sc, 60)  # 1 minute window
            broker, topic = "zookeeper:2181", "user"
            kafkaStream = KafkaUtils.createStream(ssc, broker, "user-event-streaming-consumer", {topic: 1})

            lines = kafkaStream.map(lambda x: x[1])

            #----------------------------Task 1---------------------------
            lines.pprint()
            # ------------------------------------------------------------

            lines.foreachRDD(self.run_etl_process)
            ssc.start()
            ssc.awaitTermination()
        except Exception as error:
            print(error)

    def run_etl_process(self, time, rdd):
        """
        This function is responsible to run etl releated function on user dataframe
        clean, conform data & find out some measures on fly
        """
        print("========= %s =========" % str(time))
        try:
            # Get the singleton instance of SparkSession
            sqlContext = self.getSqlContextInstance(rdd.context)
            user = sqlContext.read.json(rdd)

            if not user.rdd.isEmpty():
                # conform data by capitalize country column
                country_df = self.etl_driver.capitalize_column_value(user, "country")
                print("User Data: Records having Country with Capital Letter")
                print(country_df.show())

                ip_df =self.etl_driver.check_ip_format(country_df, "ip_address")
                print("User Data: Records having IP with correct format")
                print(ip_df.show())
                
                # conform data by change date column in one standard format
                cleaned_df = self.etl_driver.standard_date_format(country_df, "date", "dd/MM/yyyy")
                print("User Data: Records having Date With One Specified Format")
                print(cleaned_df.show())

                #  Number of unique users in the current window
                distinct_user = self.etl_driver.get_unique_user(cleaned_df, "email", "unique_users")
                print("Measure: Distinct User")
                print(distinct_user.show())
                
                #Least represented country
                country_df = cleaned_df.groupBy("country").count()
                df = self.etl_driver.get_least_represented_countries(country_df, "count")
                least_represented_countries = df.withColumnRenamed('country', "least_represented_countries")
                print("Measure: Least Represented Countries")
                print(least_represented_countries.show())
                
                #Most represented country
                df = self.etl_driver.get_most_represented_countries(country_df, "count")
                most_represented_countries = df.withColumnRenamed('country', "most_represented_countries")
                print("Measure: Most Represented Countries")
                print (most_represented_countries.show())

                # Get all females count in one minute window of batch processing...
                user_event = cleaned_df.select('id', 'first_name', to_timestamp('date') \
                                               .alias('event_date'), 'gender')
                df_user = user_event.groupBy(window("event_date", "1 minute", "1 minute"), 'id').agg(
                    count("gender") \
                        .alias(
                        "female_count")).where(F.col("female_count") == "Female")
                print("Measure: Females count in one minute window of batch processing")
                print(df_user.show(truncate=False))

        except Exception as error:
            print(error)
            raise


if __name__ == '__main__':
    kafka_consumer = KafkaConsumer()
    kafka_consumer.process_user_events()