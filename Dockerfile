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

# docker build -t my_python_image:1.0.0 . - собрать образ
# docker images - посмотреть образы
# docker run -d -p 5000:5000 --name my_python_container my_python_image:1.0.0 - запустить контейнер
# docker ps -a - посмотреть контейнеры
# docker logs dockermy_python_container - логи контейнера