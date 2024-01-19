FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /ylab_proj

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x *.sh