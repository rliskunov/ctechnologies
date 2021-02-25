FROM python:3.9-alpine
ENV FLASK_APP=app.py
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]