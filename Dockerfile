FROM python:3.9.6-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

COPY . .
RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt
EXPOSE 8000