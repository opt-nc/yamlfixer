FROM python:3.11.0a3-alpine
LABEL maintainer="michele.barre@opt.nc, jerome.alet@opt.nc, adrien.sales@opt.nc"

RUN pip install yamlfixer-opt-nc
