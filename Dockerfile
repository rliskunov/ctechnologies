FROM python:3.9.4-slim-buster
RUN apt-get -y update \
    && apt-get -y upgrade
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app .
CMD ["flask", "run"]
