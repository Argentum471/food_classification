FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install\
    libgl1\
    libgl1-mesa-glx \
    libglib2.0-0 -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN  pip3 install --upgrade pip -r requirements.txt

COPY . /app

EXPOSE 5000

ENV FLASK_APP=/app
