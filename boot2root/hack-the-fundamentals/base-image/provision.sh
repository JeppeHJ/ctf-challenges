#!/bin/bash

# Update package list
apt-get update

# Install all packages from servers
apt-get install -y \
    ufw \
    vsftpd \
    apache2 \
    ssl-cert \
    php \
    libapache2-mod-php \
    php-sqlite3 \
    php-cgi \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    perl \
    libapache2-mod-perl2 \
    ruby \
    ruby-dev \
    libcgi-pm-perl \
    apache2-suexec-pristine \
    nmap \
    openssh-server

# Clean up to reduce image size
apt-get clean
rm -rf /var/lib/apt/lists/*

# Create a version file to track when the image was created
echo "EAAA Base Image created on $(date)" > /etc/eaaa-base-image-version

echo "Base image setup completed successfully!" 