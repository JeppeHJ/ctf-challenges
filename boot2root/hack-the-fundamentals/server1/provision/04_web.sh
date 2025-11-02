#!/bin/bash

# Create a Python virtual environment
python3 -m venv /opt/webapp/venv
source /opt/webapp/venv/bin/activate

# Install Flask and dependencies
pip install -r /vagrant/webapp/requirements.txt

# Create necessary directories
mkdir -p /opt/webapp/static/{img,css,js}
mkdir -p /opt/webapp/templates
mkdir -p /opt/webapp/data

# Debug: List source directories
echo "Checking source directories:"
ls -la /vagrant/webapp/templates/
ls -la /vagrant/webapp/static/
ls -la /vagrant/webapp/src/

# Copy web application files
cp -rv /vagrant/webapp/src/* /opt/webapp/
cp -rv /vagrant/webapp/templates/* /opt/webapp/templates/
cp -rv /vagrant/webapp/static/css/* /opt/webapp/static/css/ || true
cp -rv /vagrant/webapp/static/js/* /opt/webapp/static/js/ || true
cp -rv /vagrant/webapp/static/img/* /opt/webapp/static/img/ || true

# Copy credentials.txt file
cp -v /vagrant/webapp/credentials.txt /opt/webapp/ || true

# Debug: List destination directories
echo "Checking destination directories:"
ls -la /opt/webapp/templates/
ls -la /opt/webapp/static/
ls -la /opt/webapp/

# Make the upload directory extremely permissive
chmod -R 777 /opt/webapp/static/img
chown -R www-data:www-data /opt/webapp/static/img

# Create uploads directory for profile pictures (vulnerable directory)
mkdir -p /var/www/html/uploads
chmod 777 /var/www/html/uploads
chown www-data:www-data /var/www/html/uploads

# Create a default profile picture
cp /vagrant/webapp/static/img/profile_picture.png /opt/webapp/static/img/profile_picture.png || true
# Set it as the most recent file to be the default
touch /opt/webapp/static/img/profile_picture.png

# Set proper permissions for static files
chmod -R 755 /opt/webapp/static/css
chmod -R 755 /opt/webapp/static/js
chown -R www-data:www-data /opt/webapp/static/css
chown -R www-data:www-data /opt/webapp/static/js

# Set proper permissions
chown -R www-data:www-data /opt/webapp
chmod -R 755 /opt/webapp

# Initialize the database
cd /opt/webapp && python3 db_setup.py

# Create a systemd service for the Flask application
cat > /etc/systemd/system/flask-app.service << EOF
[Unit]
Description=Flask Web Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/webapp
Environment="PATH=/opt/webapp/venv/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=development"
ExecStart=/opt/webapp/venv/bin/python -u app.py
Restart=always
StandardOutput=append:/var/log/flask-app.log
StandardError=append:/var/log/flask-app.log

[Install]
WantedBy=multi-user.target
EOF

# Create log file and set permissions
touch /var/log/flask-app.log
chown www-data:www-data /var/log/flask-app.log

# Configure Apache as a reverse proxy
a2enmod proxy
a2enmod proxy_http
a2enmod php8.3 || a2enmod php || echo "Enabling default PHP module"
a2enmod cgi
a2enmod actions
a2enmod suexec
a2enmod mime
a2enmod headers

# Enable CGI and various handlers
cat > /etc/apache2/conf-available/shell-handlers.conf << EOF
# MIME Types
AddType text/css .css
AddType application/javascript .js
AddType image/png .png
AddType image/jpeg .jpg .jpeg
AddType image/gif .gif

# PHP files
AddType application/x-httpd-php .php .php3 .php4 .php5 .php7 .phtml .phar
AddHandler application/x-httpd-php .php

# CGI scripts
AddHandler cgi-script .cgi .pl .py .rb
Action application/x-perl /usr/bin/perl
Action application/x-python /usr/bin/python3
Action application/x-ruby /usr/bin/ruby

# Shell scripts
AddHandler cgi-script .sh .bash
Action application/x-sh /bin/bash

# Make all files in upload directory executable
<Directory "/opt/webapp/static/img">
    Options +ExecCGI
    AddHandler cgi-script .php .php3 .php4 .php5 .php7 .phtml .phar .sh .bash .cgi .pl .py .rb
    
    # Serve image files properly
    <FilesMatch "\.(jpg|jpeg|png|gif)$">
        SetHandler None
        Options -ExecCGI
    </FilesMatch>
    
    # PHP files should be handled by PHP processor
    <FilesMatch "\.ph(p[3-7]?|tml|ar)$">
        SetHandler application/x-httpd-php
        Options +ExecCGI
    </FilesMatch>
    
    # Make all other files executable (for upload vulnerability)
    <FilesMatch "^(?!.*\.(jpg|jpeg|png|gif|ph(p[3-7]?|tml|ar))$).*$">
        SetHandler cgi-script
        Options +ExecCGI
    </FilesMatch>
</Directory>

# Serve static files
<Directory "/opt/webapp/static">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
    
    # Serve CSS files
    <FilesMatch "\.css$">
        SetHandler None
        ForceType text/css
        Header set Content-Type "text/css"
    </FilesMatch>
    
    # Serve JavaScript files
    <FilesMatch "\.js$">
        SetHandler None
        ForceType application/javascript
        Header set Content-Type "application/javascript"
    </FilesMatch>

    # Serve image files
    <FilesMatch "\.(jpg|jpeg|png|gif)$">
        SetHandler None
    </FilesMatch>
</Directory>
EOF

a2enconf shell-handlers

cat > /etc/apache2/sites-available/flask-app.conf << EOF
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    # Serve static files directly from Apache
    Alias /static /opt/webapp/static
    <Directory /opt/webapp/static>
        Require all granted
        Options Indexes FollowSymLinks
        AllowOverride None
        
        # Serve static files with proper MIME types
        <FilesMatch "\.(css|js|jpg|jpeg|png|gif)$">
            SetHandler None
        </FilesMatch>

        # Make executable files executable
        <FilesMatch "\.(php|py|pl|rb|sh|cgi)$">
            SetHandler cgi-script
            Options +ExecCGI
        </FilesMatch>
    </Directory>

    # Proxy all other requests to Flask
    ProxyPreserveHost On
    ProxyPass /static !
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined

    # Enable detailed error messages
    LogLevel debug
</VirtualHost>
EOF

# Enable the site and restart Apache
a2ensite flask-app
a2dissite 000-default

# Configure PHP
cat > /etc/php/*/apache2/conf.d/99-custom.ini << EOF
display_errors = On
error_reporting = E_ALL
allow_url_fopen = On
allow_url_include = On
EOF

# Restart Apache
systemctl restart apache2

# Start the Flask application
systemctl daemon-reload
systemctl enable flask-app
systemctl restart flask-app

# Check the status
systemctl status flask-app

# === PRIVILEGE ESCALATION VULNERABILITY ===

# Generate SSH key for pivoting
mkdir -p /root/.ssh
ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
chmod 600 /root/.ssh/id_rsa
chmod 644 /root/.ssh/id_rsa.pub

# Add SSH key to authorized_keys for demo purpose (normally this would be on another server)
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

# Create a README.txt with a hint about the SSH key
cat > /opt/webapp/static/img/todo.txt << EOF
- Få lukket den der anonymous access til FTP-serveren
- Få lukket den der file upload vulnerability, tænk hvis folk uploadede en reverse shell!
- Få fjernet mine ssh-credentials fra /opt/webapp/
- Få ændret så alle users ikke kan køre sudo
- Få fjernet nmap fra serveren
- Få fjernet min root ssh nøgle til den superhemmelige server fra /root-folderen her på serveren
EOF

# Set up the sudo vulnerability - allow www-data to run specific commands as root without password
cat > /etc/sudoers.d/www-data << EOF
# Allow www-data to run specific commands as root without a password
www-data ALL=(root) NOPASSWD: /usr/bin/cat, /usr/bin/find, /usr/bin/grep, /usr/bin/ls, /usr/bin/nmap
EOF

# Make sure permissions are correct
chmod 440 /etc/sudoers.d/www-data 

# Make sure static files have correct permissions and ownership
chmod -R 755 /opt/webapp/static
chown -R www-data:www-data /opt/webapp/static

# Make sure the upload directory is still writable
chmod -R 777 /opt/webapp/static/img
chown -R www-data:www-data /opt/webapp/static/img

# Configure SSH to allow password authentication
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart ssh

# Restart Apache
systemctl restart apache2

echo "Web application setup completed successfully!" 