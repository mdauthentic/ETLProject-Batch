import logging
import pathlib
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql.dataframe import DataFrame
import pyspark.sql.functions as f


spark = (
    SparkSession.builder.master("local[*]")
    .appName("Job Summary Word Count")
    .getOrCreate()
)


class DataTransformer:
    def __init__(self) -> None:
        self._spark = spark
        self._job_path = "data/jobs"
        self._trends_path = "data/gittrends"

    def _read_from_file(self) -> DataFrame:
        dir = pathlib.Path().resolve().parent / self._job_path
        return self._spark.read.json(str(dir) + "/*.json", multiLine=True)

    """Todo: Convert all to standard format
    Use the job publication dates columns
    """

    def date_converter(self):
        pass

    def wordcount_per_post(self):
        df = self._read_from_file()
        return df.withColumn(
            "wordCount", f.size(f.split(f.col("description"), " "))
        ).select("company", "wordCount")

    def word_count(self):
        """Count the words from the data fetched per day excluding stopwords"""
        df = self._read_from_file()
        tokenizer = Tokenizer(inputCol="description", outputCol="words_token")
        tokenized = tokenizer.transform(df).select("company", "words_token")
        remover = StopWordsRemover(inputCol="words_token", outputCol="words_clean")
        cleaned_df = remover.transform(tokenized).select("words_clean")
        return (
            cleaned_df.withColumn("word", f.explode(f.col("words_clean")))
            .groupBy("word")
            .count()
            .sort("count", ascending=False)
        )

    def daily_word_count(df):
        """Creates a DataFrame with word counts.
        DataFrame of (str, int): A DataFrame containing 'word' and 'count' columns.
        """
        return df.groupBy("word").count()

    def sink(self):
        """Write job data to DB"""
        return self._spark.write(self._job_path)

    def postgres_sink(df) -> None:
        logging.debug("Attempting to write data to database...")
        df.write.format("jdbc").option("url", "jdbc:postgresql:dbserver").option(
            "dbtable", "schema.tablename"
        ).option("user", "username").option("password", "password").save()
        logging.info("Data written to database table")
