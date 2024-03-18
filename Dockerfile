FROM python:alpine as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./app/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 2081

ENTRYPOINT ["python3", "main.py"]
