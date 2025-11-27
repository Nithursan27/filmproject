FROM ubuntu

ENV FLASK_APP=app
EXPOSE 8000

COPY app.py /
COPY api /api
COPY requirements.txt /

RUN apt-get update && apt-get install -y python3 python3-venv && apt-get -y install pkg-config python3-dev default-libmysqlclient-dev build-essential
RUN python3 -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

SHELL ["/bin/bash", "-c"]
CMD source .venv/bin/activate && gunicorn -b 0.0.0.0:8000 "app:create_app()"