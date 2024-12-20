FROM python:3.8.13-slim as BUILD


ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Bangkok

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends python3-opencv ffmpeg libsm6 libxext6 \ 
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip --no-cache-dir

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN rm requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]