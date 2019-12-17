FROM ubuntu:16.04

MAINTAINER zhanhui "zhanhui1987@163.com"

# set apt-get in silent installation
ENV DEBIAN_FRONTEND noninteractive

# set chinese env
ENV LANG C.UTF-8

# change apt source list
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY init/sources.list /etc/apt/sources.list

# set vim conf
COPY init/vimrc.conf /root/.vimrc

# set pip conf
RUN mkdir -p /root/.pip/
COPY init/pip.conf /root/.pip/pip.conf

# install packages
RUN \
    apt-get -y update \
    && apt-get install -y apt-utils

# set timezone
RUN \
    apt-get -y update \
    && apt-get install tzdata \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# install cron
RUN \
    apt-get -y update \
    && apt-get install -y --no-install-recommends cron

# install vim
RUN \
    apt-get -y update \
    && apt-get install -y vim

# install python3.6、python3-pip、uwsgi
RUN \
    apt-get -y update \
    && apt-get install -y python3.6 \
    && ln -s /usr/bin/python3.6 /usr/bin/python \
    && ln -s /usr/bin/python3.6 /usr/bin/python3 \
    && apt-get install -y python3-pip \
    && python3 -m pip install -U pip \
    && pip3 install uwsgi==2.0.18

# clean apt
RUN \
    apt-get remove -y python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean \
    && apt-get autoclean

# copy docker entrypoint file
COPY init/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
