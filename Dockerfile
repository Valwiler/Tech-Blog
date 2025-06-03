# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm AS base

# Create app directory
RUN mkdir -p /home/app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev openssh-client curl git \
    && apk add nano nmap jpeg-dev libwebp-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libxml2-dev libxslt-dev libxml2


# Create directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/public
RUN mkdir $APP_HOME/public
RUN mkdir $APP_HOME/public/media
RUN mkdir $APP_HOME/public/static

WORKDIR $APP_HOME

# Enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python packages
RUN pip install pip --upgrade
COPY ./requirements.txt $APP_HOME

FROM base AS requirements
RUN pip install -r requirements.txt

FROM requirements AS project_files
# Postgres Entrypoint
COPY entrypoint.sh $APP_HOME

# Copy project
COPY . $APP_HOME

RUN chmod -R 777 $APP_HOME/public/media
RUN chmod -R 777 $APP_HOME/public/static

# Change user to app
RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME


WORKDIR $APP_HOME

USER app
RUN chmod +x /home/app/web/entrypoint.sh

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

