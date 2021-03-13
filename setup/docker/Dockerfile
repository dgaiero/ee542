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
    libopenblas-dev \
    liblas-dev \
    libssl-dev \
    libgtk-3-0 \
    libgtk-3-dev \
    libavcodec-dev \
    libv4l-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    python3-smbus \
    python3-dev \
    i2c-tools \
    python3-matplotlib \
    python3-numpy \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

RUN mkdir /wheels
COPY ./wheels/* /wheels/

RUN pip install /wheels/*.whl

RUN pip install uwsgi
COPY check_opencv_version.sh check_opencv_version.sh
RUN ./check_opencv_version.sh

COPY install-nginx.sh /

RUN bash /install-nginx.sh

# Configure NGINX
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/*
# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini

# By default, run 2 processes
ENV UWSGI_CHEAPER 2

# By default, when on demand, run up to 16 processes
ENV UWSGI_PROCESSES 16

# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# By default, Nginx will run a single worker process, setting it to auto
# will create a worker for each CPU core
ENV NGINX_WORKER_PROCESSES 1

# By default, Nginx listens on port 80.
# To modify this, change LISTEN_PORT environment variable.
# (in a Dockerfile or with an option for `docker run`)
ENV LISTEN_PORT 80

# Copy start.sh script that will check for a /app/prestart.sh script and run it before starting the app
COPY start.sh /start.sh
RUN chmod +x /start.sh

# FROM base AS runtime

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static

ENV STATIC_INDEX 0

# ARG PUID
# ARG PGID
# ARG I2C_GID

# RUN groupadd -r -g $PGID frfts && useradd -u $PUID -r -s /bin/false -g frfts frfts
# RUN groupadd -r -g $I2C_GID i2c
# RUN usermod -a -G i2c frfts

# COPY --from=python-deps /.venv /.venv
# ENV PATH="/.venv/bin:$PATH"

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./uwsgi-nginx-entrypoint.sh /uwsgi-nginx-entrypoint.sh
RUN chmod +x /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]

COPY ./app /app

# RUN chown -R frfts:frfts /app
# USER frfts
ENV PYTHONPATH=/app
WORKDIR /app

CMD ["/start.sh"]
# ENTRYPOINT ["python", "app.py"]