FROM python:3.10-slim
LABEL authors="arnaudjalbert"

WORKDIR /api
COPY requirements.txt /api
RUN pip install -r requirements.txt