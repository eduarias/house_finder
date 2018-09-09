FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir house_crawler house_finder

COPY requirements.txt /
COPY house_finder/requirements.txt house_finder/
COPY house_crawler/requirements.txt house_crawler/
RUN pip install -r requirements.txt

COPY house_crawler /house_crawler
COPY house_finder /house_finder
COPY home_crawler.py scrapy.cfg /
