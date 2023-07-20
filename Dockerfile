FROM python:3.11.4-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip && pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY src /app/src

CMD ["python", "./src/app.py"]