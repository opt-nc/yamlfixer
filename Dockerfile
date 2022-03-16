FROM python:3.11.0a3-alpine
LABEL maintainer="michele.barre@opt.nc, jerome.alet@opt.nc, adrien.sales@opt.nc"


RUN pip install --upgrade pip
RUN pip install yamlfixer-opt-nc

ENV PATH="/home/worker/.local/bin:${PATH}"
