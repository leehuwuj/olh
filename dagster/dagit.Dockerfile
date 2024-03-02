FROM python:3.9-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagit dagster-postgres dagster-aws

# Copy your code and workspace to /opt/dagster/app
COPY workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY hackernews/dagster.yaml ${DAGSTER_HOME}/dagster.yaml

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]