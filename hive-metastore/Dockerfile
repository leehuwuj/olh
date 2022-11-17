# Hive 3 standalone metastore is built from Java 8
# We inherited image from the base Java 8 image of Azul zulu which is compatible for ARM users
FROM azul/zulu-openjdk:8

WORKDIR /opt

ENV HADOOP_VERSION=3.1.3
ENV METASTORE_VERSION=3.0.0

ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HIVE_HOME=/opt/apache-hive-metastore-${METASTORE_VERSION}-bin
ENV HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/*.jar:${HIVE_HOME}/lib/*.jar


RUN apt update && apt install -y curl

# Download and extract hadoop library to HADOOP_HOME
RUN curl -L https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar zxf -

# Download and extract hive standalone metastore
RUN curl -L https://repo1.maven.org/maven2/org/apache/hive/hive-standalone-metastore/${METASTORE_VERSION}/hive-standalone-metastore-${METASTORE_VERSION}-bin.tar.gz | tar zxf -
COPY metastore-site.xml ${HIVE_HOME}/conf
COPY entrypoint.sh /entrypoint.sh
RUN groupadd -r hive --gid=1000 && \
    useradd -r -g hive --uid=1000 -d ${HIVE_HOME} hive && \
    chown hive:hive -R ${HIVE_HOME} && \
    chown hive:hive /entrypoint.sh && chmod +x /entrypoint.sh

# Refresh some libraries
# Download PostgresJDBC driver for hive
RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.0.jar > ${HIVE_HOME}/lib/postgresql-42.5.0.jar
RUN rm -rf ${HIVE_HOME}/lib/guava-*.jar && \
    curl https://repo1.maven.org/maven2/com/google/guava/guava/31.1-jre/guava-31.1-jre.jar >  ${HIVE_HOME}/lib/guava-31.1-jre.jar
RUN rm -rf ${HIVE_HOME}/lib/httpcore-*.jar && \
    curl https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcore/4.4.15/httpcore-4.4.15.jar > ${HIVE_HOME}/lib/httpcore-4.4.15.jar


USER hive
EXPOSE 9083

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]