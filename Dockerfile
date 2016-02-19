FROM	ubuntu:14.04

MAINTAINER	Matt Kunkel matt@mrkunkel.com

RUN	groupadd -r homiehub && useradd -r -g homiehub homiehub

RUN	apt-get update && \
	apt-get -y upgrade

RUN	apt-get install -y python-setuptools python-dev && \
	easy_install pip

RUN	pip install pubnub influxdb

RUN	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR	/src
ADD	src/	/src

USER	homiehub

CMD python homiehub.py
