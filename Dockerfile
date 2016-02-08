FROM	ubuntu:14.04

MAINTAINER	matt@mrkunkel.com

RUN	apt-get update && \
	apt-get -y upgrade && \
	apt-get install -y python-setuptools python-dev && \
	easy_install pip && \
	pip install pubnub && \
	pip install influxdb && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD	src/	/src
WORKDIR	/src

CMD python homiehub.py
