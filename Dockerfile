FROM python:3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY dude /app/dude
WORKDIR /app

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "dude:app" ]
