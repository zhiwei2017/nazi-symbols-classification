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
RUN apt-get -y update && apt-get install ffmpeg libsm6 libxext6 curl -y
COPY poetry.lock pyproject.toml ./
RUN poetry install --with backend --no-root --no-directory

FROM base-with-dependencies

# install the project and download models from huggingface
COPY . ./
RUN poetry install && \
    curl -L https://huggingface.co/zhiwei2017/nazi-symbols-multi-class-classification/blob/main/yolo11s/yolo11s-cls.pt --output nazi_symbols_classification_backend/data/second-layer.pt &&  \
    curl -L https://huggingface.co/zhiwei2017/nazi-symbols-binary-classification/blob/main/svc/svc.pt --output nazi_symbols_classification_backend/data/first-layer.pt

EXPOSE ${API_PORT}

CMD python -m uvicorn --app-dir nazi_symbols_classification_backend --port ${API_PORT} --host 0.0.0.0 main:app