FROM python:3.10-alpine3.15

ARG IMAGE_ENV

ENV IMAGE_ENV=${IMAGE_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.3 \
  FLASK_APP=web/server \
  FLASK_ENV=development

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

RUN apk add --update nodejs npm make
RUN npm install -g sass

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers \
    && apk add libffi-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . .

RUN make build
RUN rm -r styles Makefile

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$IMAGE_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app/

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "-b", "0.0.0.0:8080", "web.server:app"]
