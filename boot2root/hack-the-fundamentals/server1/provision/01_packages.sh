#!/bin/bash

# Update package list
#apt-get update

# Install all required packages
apt-get install -y ufw vsftpd apache2 ssl-cert \
    php libapache2-mod-php php-sqlite3 php-cgi \
    python3 python3-dev python3-pip python3-venv \
    perl libapache2-mod-perl2 \
    ruby ruby-dev \
    libcgi-pm-perl \
    apache2-suexec-pristine \
    nmap openssh-server

echo "All required packages installed successfully!" 