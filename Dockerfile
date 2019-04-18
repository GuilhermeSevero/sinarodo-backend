FROM python:3.7

ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD exec gunicorn api_sinarodo.wsgi:application --bind 0.0.0.0:8080 --workers 3