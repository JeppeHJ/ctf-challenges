#!/bin/bash

# Create crown jewels file
mkdir -p /root/secret
cat > /root/secret/crownjewels.txt << EOF
=============================================================
                CONGRATULATIONS!
=============================================================

You've successfully:
1. Exploited the file upload vulnerability
2. Escalated privileges on server1
3. Discovered this secret server using nmap
4. Used the private key to SSH into this machine
5. Found the crown jewels!

Mission complete - You are a hacking master!

EAAA Cybersecurity Lab Exercise Complete
=============================================================
EOF

# Make sure root directory is secure but crown jewels file is world-readable
chmod 700 /root
chmod -R 700 /root/secret
chmod 644 /root/secret/crownjewels.txt

# Leave a hint file in the home directory
cat > /home/vagrant/README.txt << EOF
This server contains secret files.
The crown jewels can be found in /root/secret/crownjewels.txt
EOF
chmod 644 /home/vagrant/README.txt

echo "Secret files setup completed successfully!" 