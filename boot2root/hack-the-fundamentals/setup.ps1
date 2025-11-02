Write-Host "Setting up EAAA Cybersecurity Lab Environment..."

# Start the secret server first
Write-Host "Starting the secret server (server2)..."
Push-Location -Path "server2"
vagrant destroy -f
vagrant up
Pop-Location

# Start the main server
Write-Host "Starting the main server (server1)..."
Push-Location -Path "server1"
vagrant destroy -f
vagrant up
Pop-Location

# Set up SSH keys between servers
Write-Host "Setting up SSH keys between server1 and server2..."

# Get the public key from server1
Write-Host "Getting public key from server1..."
Push-Location -Path "server1"
$publicKey = vagrant ssh -c "sudo cat /root/.ssh/id_rsa.pub" -- -q
Pop-Location

# Remove any existing entries for server2 in known_hosts on server1
Write-Host "Removing existing known_hosts entries for server2 on server1..."
Push-Location -Path "server1"
vagrant ssh -c "sudo ssh-keygen -f /root/.ssh/known_hosts -R 10.0.1.20 2>/dev/null || true" -- -q
Pop-Location

# Add the public key to server2's authorized_keys
Write-Host "Adding server1's public key to server2's authorized_keys..."
Push-Location -Path "server2"
# First ensure the .ssh directory and authorized_keys file exist with proper permissions
vagrant ssh -c "sudo mkdir -p /root/.ssh && sudo touch /root/.ssh/authorized_keys && sudo chmod 700 /root/.ssh && sudo chmod 600 /root/.ssh/authorized_keys" -- -q
# Then add the key
vagrant ssh -c "echo '$publicKey' | sudo tee -a /root/.ssh/authorized_keys" -- -q
Pop-Location

# Test the connection from server1 to server2
Write-Host "Testing SSH connection from server1 to server2..."
Push-Location -Path "server1"
vagrant ssh -c "sudo ssh -o StrictHostKeyChecking=no -i /root/server2_key root@10.0.1.20 'echo Connection successful!'" -- -q
Pop-Location

Write-Host "SSH key setup completed successfully!"


Write-Host "Setup complete! The lab environment is ready."
Write-Host "Main server is at 192.168.0.10"