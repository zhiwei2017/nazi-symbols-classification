ARG PYTHON_VERSION="3.10"

FROM python:$PYTHON_VERSION-slim as base

ARG MODE="DEFAULT"
ARG WORKER_NUM=1
ARG API_PORT=8080

ENV MODE=${MODE}
ENV WEB_CONCURRENCY=${WORKER_NUM}
ENV API_PORT=${API_PORT}

WORKDIR /home

# install poetry and config it to not create virtualenv
RUN apt-get -y update && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

FROM base as base-with-dependencies

# install main dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-directory --only main

FROM base-with-dependencies

# install the project
COPY . ./
RUN poetry install --only main

EXPOSE ${API_PORT}

CMD uvicorn --app-dir nazi_symbolc_classification_backend --port ${API_PORT} --host 0.0.0.0 main:app