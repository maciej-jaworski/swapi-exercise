FROM python:3.8-slim

RUN mkdir /code
WORKDIR /code

COPY pyproject.toml /code
COPY poetry.lock /code
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --upgrade pip && pip install poetry && poetry install --no-root

ADD . /code
