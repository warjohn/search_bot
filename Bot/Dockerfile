FROM python:3.11

USER root

WORKDIR /Bot

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-pip

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 main.py

