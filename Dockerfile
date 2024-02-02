FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /ylab_proj

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
