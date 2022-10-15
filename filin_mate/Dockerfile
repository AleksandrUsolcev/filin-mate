FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "filin_mate.wsgi:application", "--bind", "0:8000" ] 

ADD entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

COPY . /app/
