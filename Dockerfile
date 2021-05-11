FROM python:latest

MAINTAINER rodolfo@superqa.com

RUN mkdir /automation

COPY ./apiTesting /automation/apiTesting
COPY ./setup.py /automation

WORKDIR /automation

RUN python3 setup.py install