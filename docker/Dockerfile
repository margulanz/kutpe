FROM python:3.12.0-alpine

# Install build dependencies
RUN apk update && \
    apk add --no-cache python3-dev gcc musl-dev linux-headers g++

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install gunicorn
ADD ./requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD ./ /app/backend
ADD ./docker /app/docker