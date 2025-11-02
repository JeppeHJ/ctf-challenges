#!/bin/bash

# Update package list
#apt-get update

# Install minimal packages
apt-get install -y openssh-server ufw

echo "Basic packages installed successfully!" 