FROM olh/spark/spark-py:base 

ENV SPARK_JARS="/opt/spark/jars/"

USER root
RUN apt update && apt install -y wget

# Add additional dependencies: aws sdk, delta, hadoop, hive
COPY jars-downloader.sh /tmp/jars-downloader.sh 
RUN chmod a+x /tmp/jars-downloader.sh && /tmp/jars-downloader.sh

# Add spark default config
COPY spark-defaults.conf /usr/local/spark-3.3.1-bin-hadoop3/conf/spark-defaults.conf

# Return to spark user
USER 185
