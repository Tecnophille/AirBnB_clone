# Configures a web server for deployment of HolbertonBnB.
# Requires sudo privileges.
# Usage: `sudo puppet apply setup_server.pp`

# Nginx configuration file
$nginx_conf = "server {
    # Use server IP as domain name
    server_name bdbnb.site www.bdbnb.site;

    # Configure root route of HolbertonBnB
    location / {
        proxy_pass http://localhost:5001/hbnb;
    }

    # Serve static content for AirBnB_clone_v4
    location /static {
        proxy_pass http://localhost:5001;
    }

    # Serve HolbertonBnB API
    location /api {
        proxy_pass http://localhost:5002/api;
    }

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/bdbnb.site/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/bdbnb.site/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if (\$host = www.bdbnb.site) {
        return 301 https://\$host\$request_uri;
    } # managed by Certbot

    if (\$host = bdbnb.site) {
        return 301 https://\$host\$request_uri;
    } # managed by Certbot

    listen      80 default_server;
    listen      [::]:80 default_server ipv6only=on;
    server_name bdbnb.site www.bdbnb.site;
    return 404; # managed by Certbot
}"

# Install Nginx
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Load Nginx configuration file
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
}

# Restart Nginx
-> exec { 'systemctl restart nginx':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Set up /data directory to host API and Flask app
file { '/data':
  ensure  => 'directory'
}

-> file { '/data/api':
  ensure => 'directory'
}

-> file { '/data/models':
  ensure => 'directory'
}

-> file { '/data/web_flask':
  ensure => 'directory'
}

-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}
