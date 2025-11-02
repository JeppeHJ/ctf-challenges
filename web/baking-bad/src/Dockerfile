# Dockerfile for web - Baking Bad
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive \
    APACHE_RUN_USER=www-data \
    APACHE_RUN_GROUP=www-data \
    APACHE_LOG_DIR=/var/log/apache2

RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php

RUN mkdir -p /var/www/bakingbad
COPY static/images/background.png /var/www/bakingbad/static/images/
COPY static/css/style.css /var/www/bakingbad/static/css/
COPY index.php /var/www/bakingbad/
COPY quality.sh /var/www/bakingbad/

RUN chmod +x /var/www/bakingbad/quality.sh

RUN chown -R www-data:www-data /var/www/bakingbad


RUN echo "brunner{d1d_1_f0rg37_70_b4n_s0m3_ch4rz?}" > /flag.txt
RUN chown -R www-data:www-data /flag.txt
RUN chmod 644 /flag.txt

EXPOSE 80

COPY bakingbad.conf /etc/apache2/sites-available/

RUN a2ensite bakingbad.conf && \
    a2dissite 000-default.conf && \
    a2enmod rewrite

CMD ["apache2ctl", "-D", "FOREGROUND"]
