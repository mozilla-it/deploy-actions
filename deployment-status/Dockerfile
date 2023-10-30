FROM python:3.10-slim

COPY ./app/ /app

RUN cd /app && pip3 install -r requirements.txt --no-cache-dir

RUN useradd -u 1021 -m app

USER app 

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
