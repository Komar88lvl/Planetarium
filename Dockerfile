FROM python:3.12-slim
LABEL maintainer="djsv91@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    just_user

RUN chown -R just_user /files/media
RUN chmod -R 755 /files/media

USER just_user
