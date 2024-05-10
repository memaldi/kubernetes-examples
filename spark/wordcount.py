from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()
sc = SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

s3_bucket = "my-bucket"
input_path = "s3a://{}/input".format(s3_bucket)
output_path = "s3a://{}/output".format(s3_bucket)

input = sc.textFile(input_path)

wordcount = input.flatMap(lambda a: a.split()).map(lambda a: (a, 1)).reduceByKey(lambda a, b: a + b)
wordcount.saveAsTextFile(output_path)
