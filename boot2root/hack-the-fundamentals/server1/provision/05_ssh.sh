#!/bin/bash

# Create SSH key pair for root user to connect to server2
echo "Creating SSH key pair for root user..."

# Create .ssh directory with proper permissions
sudo mkdir -p /root/.ssh
sudo chmod 700 /root/.ssh

# Generate SSH key pair without passphrase
sudo ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N "" -y

# Copy the private key to a more accessible location
sudo cp /root/.ssh/id_rsa /root/server2_key
sudo chmod 600 /root/.ssh/id_rsa
sudo chmod 600 /root/server2_key
sudo chmod 644 /root/.ssh/id_rsa.pub

# Remove any existing entries for server2 in known_hosts
sudo ssh-keygen -f /root/.ssh/known_hosts -R 10.0.1.20 2>/dev/null || true

# Add a note about the key in known_hosts
echo "# SSH key for server2 (10.0.1.20)" | sudo tee -a /root/.ssh/known_hosts

echo "SSH key setup completed successfully!" 