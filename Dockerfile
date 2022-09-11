FROM python:3.9-slim-bullseye as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9-slim-bullseye
WORKDIR /code
ENV EVENLESS_DB_PATH=/mail
VOLUME /mail
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN apt-get update \
    && apt-get install -y libnotmuch5 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt uvicorn
COPY ./evenless_api /code/evenless_api
CMD ["uvicorn", "evenless_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
