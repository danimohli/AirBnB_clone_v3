# Nginx installation and configuration.
# Directory structure creation for web_static deployment.
# Ownership setting for the /data directory.

# Nginx configuration file template
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://cuberule.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Ensure Nginx is installed
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} ->

# Create required directories for web_static deployment
file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->

# Create a test HTML file in the test release
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n"
} ->

# Create a symbolic link to the test release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

# Set ownership of the /data directory to the ubuntu user and group
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Ensure the /var/www and /var/www/html directories exist
file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

# Create an index.html file in the /var/www/html directory
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n"
} ->

# Create a 404.html file in the /var/www/html directory
file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
} ->

# Update the default Nginx site configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
} ->

# Restart the Nginx service to apply the new configuration
exec { 'nginx restart':
  path => '/etc/init.d/'
}
