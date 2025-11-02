#!/bin/bash

# Configure UFW
ufw default deny incoming
ufw default allow outgoing

# Allow all traffic from WiFi network
ufw allow from 10.160.0.0/24
ufw allow from 192.168.188.0/24
ufw allow from 192.168.0.0/24

# Allow SSH access
ufw allow 22/tcp

# Allow ICMP for better host discovery
ufw allow proto icmp from 10.160.0.0/24
ufw allow proto icmp from 192.168.0.0/24
ufw allow proto icmp from 192.168.188.0/24

# Allow common nmap discovery ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 21/tcp  # FTP control port

# Allow FTP passive mode ports (vsFTPd default range)
ufw allow 21100:21110/tcp  # Passive mode port range

# Allow Vagrant management network
ufw allow from 10.0.2.0/24

# Allow all outgoing traffic to secret server
ufw allow out to 10.0.1.20
ufw allow out proto icmp to 10.0.1.20  # Allow ICMP to server2
ufw allow out to 192.168.188.0/24
ufw allow out to 192.168.0.0/24
ufw allow out to 10.0.2.0/24

# Enable UFW
echo "y" | ufw enable

# Make UFW rules persistent across reboots
echo '#!/bin/sh' > /etc/rc.local
echo 'ufw enable' >> /etc/rc.local
chmod +x /etc/rc.local 