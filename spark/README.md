# Spark kubernetes
## Preparation
### Kubernetes cluster
1. Namespace  
// TODO: 
2. Service account  
// TODO: 
### Docker image
1. Build base spark image
- From your host machine, move to SPARK_HOME project and build the base image (python binding support):
```shell
cd $SPARK_HOME && docker build -t spark:base-3.3.1 -f kubernetes/dockerfiles/spark/bindings/python/Dockerfile .
```
2. Move back to this directory and build new spark image which expands from the above base image and add supports for delta lake.
```shell
docker build -t spark:base -f Dockerfile .
```

## Submit spark app to kubernetes cluster
- Run spark-submit which target cluster to k8s:
```shell
spark-submit \
    --deploy-mode cluster \
    --master k8s://https://kubernetes.docker.internal:6443 \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark:base \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///tmp/spark-examples_2.12-3.3.1.jar
```

- We can better submit the Spark job defined from S3:
```shell
spark-submit \
    --deploy-mode cluster \
    --master k8s://[CHANGE_ME] \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=spark:base \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.hadoop.fs.s3a.endpoint=[CHANGE_ME]\
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \
    --conf spark.hadoop.fs.s3a.access.key=[CHANGE_ME] \
    --conf spark.hadoop.fs.s3a.secret.key=[CHANGE_ME] \
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.hadoop.fs.s3a.fast.upload=true \
    s3a://<bucket>/<jar/python/path>
```


- Check k8s job:
```shell
(base) ➜ kubectl -n spark get pod
NAME                               READY   STATUS        RESTARTS   AGE
spark-pi-167abb84a59fcca8-driver   0/1     Completed     0          7s
spark-pi-e1323b84a59fd7e0-exec-1   0/1     Terminating   0          4s
spark-pi-e1323b84a59fd7e0-exec-2   0/1     Terminating   0          4s
```
