FROM ubuntu:14.04

MAINTAINER rmz "rmz@rmz.no"

# Update and install misc. toosl we need
RUN apt-get update -y -qq

RUN apt-get install -y -qq tar git curl nano wget dialog net-tools build-essential

# Install pip's dependency: setuptools:
RUN apt-get install -y python python-dev python-distribute python-pip


EXPOSE 80
EXPOSE 5000

# Download and install Flask framework:
RUN  pip install flask
WORKDIR /controlmeta
COPY  controlmeta  /controlmeta
RUN  pip install -r /controlmeta/requirements.txt

RUN  python app.py
CMD [ -f /.pip/pip.log && cat /.pip/pip.log ]

