#!/bin/bash

echo "Setting up EAAA Cybersecurity Lab Environment..."

# Start the secret server (server2) first
echo "Starting the secret server (server2)..."
cd server2
vagrant destroy -f
vagrant up
cd ..

# Start the main server (server1)
echo "Starting the main server (server1)..."
cd server1
vagrant destroy -f
vagrant up
cd ..

# Set up SSH keys between the servers
echo "Setting up SSH keys between server1 and server2..."

# Get the public key from server1
echo "Getting public key from server1..."
PUBLIC_KEY=$(vagrant ssh -c "sudo cat /root/.ssh/id_rsa.pub" -- -q)

# Remove any existing entries for server2 in known_hosts on server1
echo "Removing existing known_hosts entries for server2 on server1..."
vagrant ssh -c "sudo ssh-keygen -f /root/.ssh/known_hosts -R 10.0.1.20" -- -q

# Ensure .ssh directory and authorized_keys file exist on server2 with correct permissions
echo "Adding server1's public key to server2's authorized_keys..."
cd server2
vagrant ssh -c "
sudo mkdir -p /root/.ssh
sudo touch /root/.ssh/authorized_keys
sudo chmod 700 /root/.ssh
sudo chmod 600 /root/.ssh/authorized_keys
echo '$PUBLIC_KEY' | sudo tee -a /root/.ssh/authorized_keys
" -- -q
cd ..

# Test the SSH connection from server1 to server2
echo "Testing SSH connection from server1 to server2..."
cd server1
vagrant ssh -c "sudo ssh -o StrictHostKeyChecking=no -i /root/server2_key root@10.0.1.20 'echo Connection successful!'" -- -q
cd ..

echo "SSH key setup completed successfully!"

echo "Setup complete! The lab environment is ready."
echo "Main server is at 172.16.0.10" 