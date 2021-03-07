FROM ubuntu:18.04

MAINTAINER Sebastien Danthinne "sdanthinne@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN python3 --version

RUN pip3 install --upgrade "pip < 21.0"

RUN pip3 install -r requirements.txt

RUN mkdir /app

COPY app /app/

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ]

