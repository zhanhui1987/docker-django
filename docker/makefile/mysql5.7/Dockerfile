FROM mysql:5.7

MAINTAINER zhanhui "zhanhui1987@163.com"

ENV LANG C.UTF-8

# change timezone
ENV TZ=Asia/Shanghai

# copy database init script: init.sql to /docker-entrypoint-initdb.d floder.
COPY init/init.sql /docker-entrypoint-initdb.d

# copy mysql conf file
COPY init/mysql.cnf /etc/mysql/my.cnf
