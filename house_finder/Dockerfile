FROM python:3.6-alpine3.8

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache build-base postgresql-libs postgresql-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /house_finder
WORKDIR /house_finder
RUN chmod +x docker-entrypoint.sh create_superadmin.py

ENV DJANGO_SU_USERNAME admin
ENV DJANGO_SU_EMAIL admin@example.org
ENV DJANGO_SU_PASSWORD test1234

