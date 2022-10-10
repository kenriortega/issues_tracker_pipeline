FROM apache/airflow:2.4.0
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
         librdkafka-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark==2.1.3
RUN pip install --no-cache-dir apache-airflow-providers-docker==2.5.1
RUN pip install --no-cache-dir jira pandas kafka-python