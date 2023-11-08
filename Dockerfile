FROM python:3.10.11

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

COPY /requirements.txt /
COPY /config/.vscode /project/
COPY /config/config.toml /project/

RUN pip install -r /requirements.txt

EXPOSE 8888

COPY docker/docker-entrypoint.sh /
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
