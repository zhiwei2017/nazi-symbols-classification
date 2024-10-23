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
RUN poetry install --with dev,test,docs,nb,backend --no-root --no-directory

FROM base-with-dependencies

# install the project and download models from huggingface
COPY . ./
RUN poetry install && \
    curl -L https://huggingface.co/zhiwei2017/yolo11s-cls-nazi-symbols/resolve/main/yolo11s-cls-multiple-nazi-symbols/weights/best.pt --output nazi_symbols_classification_backend/data/second-layer.pt &&  \
    curl -L https://huggingface.co/zhiwei2017/yolo11s-cls-nazi-symbols/resolve/main/yolo11s-cls-nazi-symbol-detection/weights/best.pt --output nazi_symbols_classification_backend/data/first-layer.pt

EXPOSE ${API_PORT}

CMD python -m uvicorn --app-dir nazi_symbols_classification_backend --port ${API_PORT} --host 0.0.0.0 main:app