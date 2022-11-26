spark-submit \
    --deploy-mode cluster \
    --master k8s://https://kubernetes.docker.internal:6443 \
    --name "TweetsFact pipeline" \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark:base \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.hadoop.fs.s3a.endpoint=http://kubernetes.docker.internal:9000 \
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \
    --conf spark.hadoop.fs.s3a.access.key=[CHANGE_ME] \
    --conf spark.hadoop.fs.s3a.secret.key=[CHANGE_ME] \
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.hadoop.fs.s3a.fast.upload=true \
    --conf spark.kubernetes.driverEnv.HIVE_METASTORE_URIS=thrift://kubernetes.docker.internal:9083 \
    s3a://[CHANGE_ME].py