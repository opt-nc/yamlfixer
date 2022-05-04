FROM python:3.11.0a7-alpine
LABEL maintainer="michele.barre@opt.nc, jerome.alet@opt.nc, adrien.sales@opt.nc"


RUN pip install --upgrade pip
RUN pip install https://github.com/opt-nc/yamlfixer/archive/main.tar.gz

ENV PATH="/home/worker/.local/bin:${PATH}"
