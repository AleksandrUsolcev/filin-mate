FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
