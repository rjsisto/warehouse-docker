FROM python:3.11-slim-buster

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

COPY /requirements.txt /
COPY /config.py /

RUN pip install -r /requirements.txt

EXPOSE 8888

COPY docker/docker-entrypoint.sh /
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
