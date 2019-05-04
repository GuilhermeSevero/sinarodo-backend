FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /config && mkdir /logs && chmod +w /logs

ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8080

ADD run_api.sh /run_api.sh
RUN chmod +x /run_api.sh

CMD /run_api.sh