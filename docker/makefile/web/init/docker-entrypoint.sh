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

# init mysql table for django and create default superuser
django_manage_file="/root/docker-django/z1987_web/manage.py"
if [ -f ${django_manage_file} ];
then
    /usr/bin/python ${django_manage_file} makemigrations app_blog
    /usr/bin/python ${django_manage_file} migrate

    # create superuesr for django
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | /usr/bin/python ${django_manage_file} shell
fi

# create a process that cannot be ended
tail -f /dev/null

