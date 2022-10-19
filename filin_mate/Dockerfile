FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["gunicorn", "filin_mate.wsgi:application", "--bind", "0:8000" ] 

COPY . /app/
