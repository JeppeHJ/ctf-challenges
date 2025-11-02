# EAAA Cybersecurity Lab Environment

This is a fun little hacking-lab developed for students of Erhvervsakademi Aarhus with little to no experience with cyber security.
This lab has two systems to hack and provides a reasonably realistic hacking experience and introduces participants to fundamentals of networking, Linux, enumeration, and web exploitation. 

It has been specifically developed to be ultra-easy to spin up. Enter a few commands in the terminal and have the lab running in a few minutes, ready to be hacked by participants!

## Lab Environment Details

### Server1 (Main server - 172.16.0.10)
- Web server hosting a web application
- FTP server
- Multiple intentionally vulnerable components for training and several attack paths

### Server2 (Internal "secret" server - 10.0.1.20)
- SSH running
- Hidden server with "crown jewels"
- Only accessible through Server1

## Prerequisites for hosting the lab

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Windows Setup

1. Clone or download this repository
2. Open PowerShell as Administrator
3. Navigate to the repository directory
4. Create the base image:
   ```powershell
   cd base-image
   vagrant up
   vagrant package --output eaaa-base.box
   vagrant box add eaaa-base.box --name eaaa-base
   cd ..
   ```
5. Run the setup script:
   ```powershell
   ./setup.ps1
   ```

## Linux/MacOS Setup

1. Clone or download this repository
2. Open a terminal
3. Navigate to the repository directory
4. Create the base image:
   ```bash
   cd base-image
   vagrant up
   vagrant package --output eaaa-base.box
   vagrant box add eaaa-base.box --name eaaa-base
   cd ..
   ```
5. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
6. Run the setup script:
   ```bash
   ./setup.sh
   ```
   
## TO DO
- Implement mechanisms to make it more flexible/stable for scenarios with several participants (some attack paths in the environment may cause disruption for other participants)

## Maintenance and changes

When updating or changing the lab environment:
1. Make changes to the server configurations
2. If package changes are needed, update the base image:
   ```bash
   cd base-image
   # Make changes to provision.sh
   vagrant up
   vagrant package --output eaaa-base.box
   vagrant box remove eaaa-base
   vagrant box add eaaa-base.box --name eaaa-base
   cd ..
   ```
3. Run the setup script again

## If you for whatever reason want to set it up without using the base image

### Windows - without EAAA Base Image

1. Clone or download this repository
2. Open PowerShell as Administrator
3. Navigate to the repository directory
4. Edit the Vagrantfiles in server1 and server2 to use the default Ubuntu box:
   - In server1/Vagrantfile, comment out `config.vm.box = "eaaa-base"` and uncomment the Ubuntu box lines
   - In server2/Vagrantfile, do the same
5. Run the setup script:
   ```powershell
   ./setup.ps1
   ```
   
### Linux/MacOS - without EAAA Base Image

1. Clone or download this repository
2. Open a terminal
3. Navigate to the repository directory
4. Edit the Vagrantfiles in server1 and server2 to use the default Ubuntu box:
   - In server1/Vagrantfile, comment out `config.vm.box = "eaaa-base"` and uncomment the Ubuntu box lines
   - In server2/Vagrantfile, do the same
5. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
6. Run the setup script:
   ```bash
   ./setup.sh
   ```
