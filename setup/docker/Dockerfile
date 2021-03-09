FROM python:3.9 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    yasm \
    pkg-config \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavformat-dev \
    libpq-dev \
    libssl-dev \
    libavcodec-dev \
    libv4l-dev \
    python3-smbus \
    python3-dev \
    i2c-tools \
    python3-matplotlib \
    python3-numpy \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

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