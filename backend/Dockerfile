FROM python:3.12-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8

ARG PY_SHORT_VERSION=3.12

FROM base AS builder

WORKDIR /
RUN apt-get update && \
    apt-get install -y gcc gdal-bin g++ libgdal-dev python3-gdal
RUN pip install --upgrade pip

COPY pyproject.toml uv.lock ./

RUN pip install uv
RUN uv sync

FROM base AS runtime

ENV PYTHONPATH="/app"
ENV PATH="/.venv/bin:$PATH"

COPY --from=builder /.venv /.venv

RUN useradd --no-create-home appuser

WORKDIR /app

USER appuser
