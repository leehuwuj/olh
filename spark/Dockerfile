FROM pyspark:base-3.3.1 

ENV SPARK_JARS="/opt/spark/jars/"

USER root
RUN apt update && apt install -y wget

# Add additional dependencies: aws sdk, delta, hadoop, hive
COPY test/jars-downloader.sh /tmp/jars-downloader.sh 
RUN chmod a+x /tmp/jars-downloader.sh && /tmp/jars-downloader.sh

# Return to spark user
USER 185
