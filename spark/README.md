# Spark kubernetes
## Preparation
### Kubernetes cluster
- Make sure your kubernetes cluster is available and there is an namespace for Spark.
```
kubectl create namespace spark
```

- Update Spark manifest corespond to your environment (host mount volume path, cpu and ram resources,...)

- Apply the k8s resources for Spark:
```
kubectl -n spark apply -f manifests
```


### Docker image
1. Build base spark image
- From your host machine, move to SPARK_HOME project and build the base image (python binding support):
```shell
cd $SPARK_HOME && ./bin/docker-image-tool.sh -r olh -t base -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

2. Move back to this directory and build new spark image which expands from the above base image and adding supports for delta lake.
```shell
docker build -t olh/spark:delta -f Dockerfile .
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
    --conf spark.kubernetes.container.image=olh/spark:delta \
    --conf spark.kubernetes.namespace=spark \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///tmp/spark-examples_2.12-3.3.1.jar
```

- We can better submit the Spark job defined from MinIO:
```shell
spark-submit \
    --deploy-mode cluster \
    --master k8s://[CHANGE_ME] \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=olh/spark:delta \
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

> Note that, there are already default configurations which we defined in Spark image, please check them in spark-defaults.conf files. So actually, you dont need to specify them when submiting. I just put them here for the case you wanna overwrite the default config when submitting. 

- Check k8s job:
```shell
(base) ➜ kubectl -n spark get pod
NAME                               READY   STATUS        RESTARTS   AGE
spark-pi-167abb84a59fcca8-driver   0/1     Completed     0          7s
spark-pi-e1323b84a59fd7e0-exec-1   0/1     Terminating   0          4s
spark-pi-e1323b84a59fd7e0-exec-2   0/1     Terminating   0          4s
```
