FROM mohaseeb/raspberrypi3-python-opencv:3.4.2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
     apt-get install -y --force-yes python3-pip python3-dev

 COPY ./requirements.txt /requirements.txt

RUN pip install opencv-python
COPY check_opencv_version.sh check_opencv_version.sh
RUN ./check_opencv_version.sh


# FROM base AS runtime

RUN mkdir /app

ARG PUID
ARG PGID
ARG I2C_GID

RUN groupadd -r -g $PGID frfts && useradd -u $PUID -r -s /bin/false -g frfts frfts
# RUN groupadd -r -g $I2C_GID i2c
# RUN usermod -a -G i2c frfts

# COPY --from=python-deps /.venv /.venv
# ENV PATH="/.venv/bin:$PATH"

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

RUN chown -R frfts:frfts /app
USER frfts
WORKDIR /app

ENTRYPOINT ["python", "app.py"]





# FROM ubuntu:18.04

# MAINTAINER Sebastien Danthinne "sdanthinne@gmail.com"

# ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update -y && \
#     apt-get install -y python3-pip python3-dev python3-opencv

# COPY ./requirements.txt /requirements.txt

# WORKDIR /

# RUN python3 --version

#RUN pip3 install --upgrade "pip < 21.0"

#RUN pip3 install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt
 RUN mkdir /app

 COPY app /app/

 ENTRYPOINT [ "python" ]

 CMD [ "app/app.py" ]

