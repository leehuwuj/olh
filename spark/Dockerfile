FROM olh/spark-py:base 

ENV SPARK_JARS="/opt/spark/jars/"

USER root
RUN apt update && apt install -y wget

# Add additional dependencies: aws sdk, delta, hadoop, hive
COPY jars-downloader.sh /tmp/jars-downloader.sh 
RUN chmod a+x /tmp/jars-downloader.sh && /tmp/jars-downloader.sh

# Add spark default config
COPY spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf

# Add hive-site.xml to indicate Spark to use external metastore.
# This config is required but it's able to override when you
# submit spark to kubernetes by mount a configmap
COPY hive-site.xml ${SPARK_HOME}/conf/hive-site.xml

# Return to spark user
USER 185
