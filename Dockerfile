FROM python:slim

RUN mkdir /app /app/data

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY manage.py gunicorn.conf.py entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
COPY herodotus/ /app/herodotus/


EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]