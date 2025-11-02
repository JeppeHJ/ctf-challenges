#!/bin/bash

# Set up SSH for server1 access
echo "Setting up SSH for server1 access..."

# Create .ssh directory and authorized_keys file if they don't exist
sudo mkdir -p /root/.ssh
sudo touch /root/.ssh/authorized_keys
sudo chmod 700 /root/.ssh
sudo chmod 600 /root/.ssh/authorized_keys

# Add a note to the authorized_keys file about where the key is from
echo "# SSH key from server1 (10.0.1.10)" | sudo tee -a /root/.ssh/authorized_keys

# Configure SSH to allow root login with key
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Add StrictHostKeyChecking=no to ssh_config to avoid host key verification issues
sudo mkdir -p /root/.ssh
sudo tee /root/.ssh/config << EOF
Host 10.0.1.10
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
EOF
sudo chmod 600 /root/.ssh/config

# Restart SSH service
sudo systemctl restart ssh

echo "SSH setup completed successfully!" 