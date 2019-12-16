#!/bin/bash

# start uwsgi
uwsgi_file="/root/docker-django/z1987_web/z1987_web_uwsgi.ini";
if [ -f ${uwsgi_file} ];
then
    /usr/local/bin/uwsgi --ini ${uwsgi_file};
fi

# start cron service
service cron start;

# init crontab
cron_init_file="/root/docker-django/z1987_web/sysadmin/cron/README";
if [ -f ${cron_init_file} ];
then
    crontab < ${cron_init_file};
    service cron restart;
fi

# create a process that cannot be ended
tail -f /dev/null
