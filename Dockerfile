FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .