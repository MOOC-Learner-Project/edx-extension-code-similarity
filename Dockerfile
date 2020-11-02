FROM php:7.1-apache

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install -y python3 python3-pip
RUN pip3 install scipy pyflakes

COPY scripts/compare_trajectories.py /scripts/compare_trajectories.py
COPY scripts/common.py /scripts/common.py
COPY data/STORAGE /data/STORAGE
COPY scripts/test_compare_trajectories.py /scripts/test_compare_trajectories.py
COPY scripts/test_count_keywords.py /scripts/test_count_keywords.py

RUN export PYTHONPATH=/scripts/:$PYTHONPATH

RUN ["python3", "/scripts/test_compare_trajectories.py"]
RUN ["python3", "/scripts/test_count_keywords.py"]

COPY server.crt /etc/apache2/ssl/server.crt
COPY server.key /etc/apache2/ssl/server.key
COPY dev.conf /etc/apache2/sites-enabled/dev.conf
COPY .htaccess /var/www/html/

COPY results.py /usr/lib/cgi-bin/
RUN chmod 755 /usr/lib/cgi-bin/results.py

COPY html/ /var/www/html/

RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2enmod cgi
RUN service apache2 restart

