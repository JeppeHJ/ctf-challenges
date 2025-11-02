#!/bin/bash

# Ensure ftp user exists and set up FTP directory
useradd -r -m -d /srv/ftp ftp || true
mkdir -p /srv/ftp
echo "hans@eaaa.dk" > /srv/ftp/secret.txt
echo "kBaqIR2Bkle%YZnZq5hK" >> /srv/ftp/secret.txt
chown -R ftp:nogroup /srv/ftp
chmod 555 /srv/ftp
chmod 444 /srv/ftp/secret.txt

# Simple vsftpd configuration
cat > /etc/vsftpd.conf << EOF
listen=YES
anonymous_enable=YES
no_anon_password=YES
anon_root=/srv/ftp
write_enable=NO
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES

# Passive mode configuration
pasv_enable=YES
pasv_min_port=21100
pasv_max_port=21110
pasv_address=10.160.0.120
EOF

# Restart vsftpd
systemctl restart vsftpd 