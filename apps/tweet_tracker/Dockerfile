# Dockerfile
FROM python:3.8

WORKDIR /
# creating the file to write XComs to https://docs.astronomer.io/learn/kubepod-operator
RUN mkdir -p airflow/xcom
RUN echo "" > airflow/xcom/return.json

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

ENV BOOSTRAP_SERVERS=""

ENTRYPOINT ["python","./main.py"]
