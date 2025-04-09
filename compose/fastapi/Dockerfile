FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN apt-get update -y \
  && apt-get install gcc -y

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY ./src /app/src
COPY ./src/main.py /app/main.py

COPY ./alembic /app/alembic
COPY ./alembic.ini /app/

COPY ./compose/fastapi/prestart.sh .

WORKDIR /app/src
