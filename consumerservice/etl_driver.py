import functools
from pyspark.sql.functions import *
from pyspark.sql import functions as F


class ETLDriver(object):

    def capitalize_column_value(self, dataframe, column_name):
        """
        Get the Spark Dataframe and convert first letter of country column in caps.

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name which values need to be capitalized
        :type column_name: string
        :return: dataframe after converting column value in caps
        :rtype: SparkDataframe
        """
        df = (functools.reduce(lambda memo_df, col_name: memo_df.withColumn(col_name,
                                                                                   initcap(col(col_name))),
                                      [column_name], dataframe))
        return df

    def standard_date_format(self, dataframe, column_name, format):
        """
        Get the Spark Dataframe and convert date in a provided date format.

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name which values need to be convert in standart specified format
        :type column_name: string
        :param format: date format
        :type format: string
        :return: dataframe after converting column values standard date format
        :rtype: SparkDataframe
        """
        date_df = dataframe.withColumn('new_date',to_date(col(column_name), format))
        df = date_df.drop(column_name).withColumnRenamed('new_date', column_name)
        return df

    def get_unique_user(self, dataframe, column_name, column_alias):
        """
        Get the Spark Dataframe and find out unique users in currrent batch

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name from which need to findout distinct values
        :type column_name: string
        :param column_alias: column alias
        :type column_alias: string
        :return: dataframe having unique users
        :rtype: SparkDataframe
        """
        df = dataframe.agg(countDistinct(col(column_name)).alias(column_alias))
        return df

    def get_least_represented_countries(self, dataframe, column_name):
        """
        Get the Spark Dataframe and find out all the countries which has minimum repeated value in country column

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name from which need to get the least repeated countries
        :type column_name: string
        :return: dataframe having all countries which has minimum count value in country column
        :rtype: SparkDataframe
        """
        least_represented = dataframe.select(F.min(F.col(column_name)).alias("MIN")).limit(1).collect()[0].MIN
        df = dataframe.select(F.col("*")).filter(F.col(column_name) == least_represented)
        return df

    def get_most_represented_countries(self, dataframe, column_name):
        """
        Get the Spark Dataframe and find out all the countries which has maximum repeated value in country column

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name from which need to get the most repeated countries
        :type column_name: string
        :return: dataframe having all countries which has maximum count value in country column
        :rtype: SparkDataframe
        """
        most_represented = dataframe.select(F.max(F.col(column_name)).alias("MAX")).limit(1).collect()[0].MAX
        df = dataframe.select(F.col("*")).filter(F.col(column_name) == most_represented)
        return df
        
    def check_ip_format(self, dataframe, column_name):
        """
        Get the Spark Dataframe and filter out all records which don't have right IP format

        :param dataframe: spark dataframe containing user records
        :type dataframe: dataframe
        :param column_name: column name
        :type column_name: string
        :return: dataframe having all records with right ip format
        :rtype: SparkDataframe
        """
        df = dataframe.select(F.col("*")).where(col(column_name).like("%.%.%.%"))
        return df

