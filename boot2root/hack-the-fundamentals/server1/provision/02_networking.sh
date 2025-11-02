# Create hans user with password
useradd -m -s /bin/bash hans
echo "hans:EaaaErEnGodSkole123" | chpasswd

# Add hans to sudo group with NOPASSWD option
usermod -aG sudo hans
echo "hans ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/hans
chmod 440 /etc/sudoers.d/hans

# Create todo.txt in hans' home directory
cat > /home/hans/todo.txt << EOF
- Få lukket den der anonymous access til FTP-serveren
- Få lukket den der file upload vulnerability, tænk hvis folk uploadede en reverse shell!
- Få fjernet mine ssh-credentials fra /opt/webapp/
- Få ændret så alle users ikke kan køre sudo
- Få fjernet nmap fra serveren
- Få fjernet min root ssh nøgle til den superhemmelige server fra /root-folderen her på serveren
EOF

# Set proper permissions
chown hans:hans /home/hans/todo.txt
chmod 644 /home/hans/todo.txt

# Create a duplicate of todo.txt at the root level
cp /home/hans/todo.txt /todo.txt
chmod 644 /todo.txt

# Configure network interface names
cat > /etc/netplan/01-netcfg.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: true
      dhcp6: true
      match:
        macaddress: $(ip link show enp0s3 | grep -o "..:..:..:..:..:.." | head -1)
      set-name: vagrant-mgmt
    enp0s8:
      addresses: [192.168.0.10/24]
      match:
        macaddress: $(ip link show enp0s8 | grep -o "..:..:..:..:..:.." | head -1)
      set-name: public-net
    enp0s9:
      addresses: [10.0.1.10/24]
      match:
        macaddress: $(ip link show enp0s9 | grep -o "..:..:..:..:..:.." | head -1)
      set-name: internal-net
EOF

# Apply netplan configuration
netplan apply