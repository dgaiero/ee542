FROM mohaseeb/raspberrypi3-python-opencv:3.4.2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
     apt-get install -y --force-yes python3-pip python3-dev

 COPY ./requirements.txt /requirements.txt

 WORKDIR /
 RUN python --version

#RUN pip3 install --upgrade "pip < 21.0"

#RUN pip3 install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt
 RUN mkdir /app

 COPY app /app/

 ENTRYPOINT [ "python" ]

 CMD [ "app/app.py" ]

