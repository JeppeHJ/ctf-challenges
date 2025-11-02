#!/bin/bash

# Configure firewall - allow all traffic from Kali, main server, and Vagrant
ufw default deny incoming
ufw default allow outgoing

# Allow all traffic from Kali and main server (both TCP and UDP)
ufw allow proto tcp from 192.168.188.0/24 to any
ufw allow proto udp from 192.168.188.0/24 to any
ufw allow proto tcp from 192.168.0.10 to any
ufw allow proto udp from 192.168.0.10 to any

# Allow ICMP from server1 for better host discovery
ufw allow proto icmp from 10.0.1.10 to any

# Allow common nmap discovery ports from server1
ufw allow proto tcp from 10.0.1.10 to any port 22
ufw allow proto tcp from 10.0.1.10 to any port 80
ufw allow proto tcp from 10.0.1.10 to any port 443

# Allow Vagrant management network
ufw allow from 10.0.2.0/24

# Make sure SSH is explicitly allowed
ufw allow 22/tcp

echo "y" | ufw enable

echo "Firewall configuration completed successfully!" 