FROM ubuntu:16.04

MAINTAINER zhanhui "zhanhui1987@163.com"

# change apt source list file
COPY init/sources.list /etc/apt/sources.list

# update apt
RUN apt-get update

# change time zone
RUN apt-get install -y tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# install nginx
RUN apt-get install -y nginx

# clean apt files
RUN apt-get autoclean \
    && apt-get clean \
    && apt-get remove \
    && rm -rf /var/lib/apt/lists/*

# make the docker container work
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# rm nginx default conf file
RUN rm -rf /etc/nginx/sites-enabled/default

EXPOSE 80 443

ENTRYPOINT /usr/sbin/nginx
