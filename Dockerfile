FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh