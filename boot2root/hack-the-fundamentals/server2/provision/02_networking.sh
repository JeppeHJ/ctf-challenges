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
      addresses: [10.0.1.20/24]
      match:
        macaddress: $(ip link show enp0s8 | grep -o "..:..:..:..:..:.." | head -1)
      set-name: internal-net
EOF

# Apply netplan configuration
netplan apply