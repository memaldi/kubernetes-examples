from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()
sc = SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

access_key = "access-key"
secret_key = "secret-key"
s3_bucket = "my-bucket"
minio_endpoint = "http://minio.minio.svc.cluster.local:9000"
input_path = "s3a://{}/input".format(s3_bucket)
output_path = "s3a://{}/output".format(s3_bucket)

spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", minio_endpoint)
spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")

input = sc.textFile(input_path)

wordcount = input.flatMap(lambda a: a.split()).map(lambda a: (a, 1)).reduceByKey(lambda a, b: a + b)
wordcount.saveAsTextFile(output_path)
