#!bin/sh

declare -a JARS=(
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.319/aws-java-sdk-bundle-1.12.319.jar \
    https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.1.1/delta-core_2.12-2.1.1.jar \
    https://repo1.maven.org/maven2/io/delta/delta-storage/2.1.1/delta-storage-2.1.1.jar \
    https://repo1.maven.org/maven2/com/google/inject/guice/4.0/guice-4.0.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.2/hadoop-aws-3.2.2.jar \
    https://repo1.maven.org/maven2/org/apache/hive/hive-common/3.1.3/hive-common-3.1.3.jar \
    https://repo1.maven.org/maven2/org/apache/hive/hive-exec/3.1.3/hive-exec-3.1.3.jar \
    https://repo1.maven.org/maven2/org/apache/hive/hive-metastore/3.1.3/hive-metastore-3.1.3.jar \
    https://repo1.maven.org/maven2/org/apache/hive/hive-serde/3.1.3/hive-serde-3.1.3.jar
)

if [[ -z "${SPARK_JARS}" ]];
then
    echo "SPARK_JARS environment variable is not set!"
    exit 1
fi

for jar in "${JARS[@]}"
do
    wget $jar -P $SPARK_JARS
done
