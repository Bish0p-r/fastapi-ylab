FROM python:3.11-slim

RUN mkdir /fastapi-ylab

WORKDIR /fastapi-ylab

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .