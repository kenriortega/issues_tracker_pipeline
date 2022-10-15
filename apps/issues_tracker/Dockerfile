# Dockerfile
FROM python:3.8

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

ENV BOOSTRAP_SERVERS=""
ENV GITHUB_TOKEN=""

ENTRYPOINT ["python","./main.py"]
