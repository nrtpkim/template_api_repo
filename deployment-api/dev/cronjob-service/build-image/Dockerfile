FROM python:3.7.13-slim as BUILD


ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Bangkok

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends python3-opencv ffmpeg libsm6 libxext6 \ 
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip --no-cache-dir

WORKDIR /app

ADD cronjob/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN rm requirements.txt