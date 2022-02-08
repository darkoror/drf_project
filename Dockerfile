FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && \
    apt-get install -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# set work dir
WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock /usr/src/app/

RUN pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy && \
    rm -rf /root/.cache/pipenv && \
    pip uninstall -y pipen

COPY entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

EXPOSE 8000
