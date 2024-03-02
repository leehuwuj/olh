ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION

# ==> Add Dagster layer
RUN \
    pip install \
        dagster==${DAGSTER_VERSION} \
        dagster-postgres \
        dagster-aws \
        dagster-k8s

# ==> Add user code layer
# Example pipelines
COPY setup.py setup.py
COPY setup.cfg setup.cfg
RUN pip install ".[dev]" \
    &&  rm -rf /var \
    &&  rm -rf /root/.cache  \
    &&  rm -rf /usr/lib/python2.7 \
    &&  rm -rf /usr/lib/x86_64-linux-gnu/guile

ARG DAGSTER_HOME=/opt/dagster
ENV DAGSTER_HOME=${DAGSTER_HOME}
RUN mkdir -p ${DAGSTER_HOME}

WORKDIR ${DAGSTER_HOME}

COPY hackernews hackernews
COPY dagster.yaml .