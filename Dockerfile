FROM python:3.11.0a3-alpine
LABEL maintainer="michele.barre@opt.nc, jerome.alet@opt.nc"

COPY yamlfixer /usr/local/bin/yamlfixer
COPY requirements.txt /requirements.txt

RUN chmod 0755 /usr/local/bin/yamlfixer
RUN pip install -r /requirements.txt
