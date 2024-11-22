FROM python:3.10-slim
LABEL authors="arnaudjalbert"

WORKDIR /pebble
COPY requirements.txt /pebble
RUN pip install -r requirements.txt
COPY . /pebble

ENV PYTHONPATH=/pebble/app