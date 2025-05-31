FROM python:3.10-slim-buster

WORKDIR /root
ADD /docker/requirements.txt /root/requirements.txt
RUN pip3 install --user --no-cache-dir -r requirements.txt

RUN mkdir -p /movie_search
WORKDIR /movie_search