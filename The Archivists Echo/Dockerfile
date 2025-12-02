# Use the official PHP 8.3 Apache image (Debian-based)
FROM php:8.3-apache

# Install necessary tools for archive handling and cleanup
RUN apt-get update && apt-get install -y \
    zip \
    unzip \
    bzip2 \
    libarchive-tools \
    unrar-free \
 && rm -rf /var/lib/apt/lists/*

# Enable headers module and add security config
COPY 000-security.conf /etc/apache2/conf-available/000-security.conf
RUN a2enmod headers && a2enconf 000-security

# Set the working directory
WORKDIR /var/www/html

# Copy custom PHP configuration
COPY php.ini /usr/local/etc/php/conf.d/custom-php.ini

# Copy application files
COPY web/ ./

# Copy the flag into the container
COPY flag.txt /flag.txt

# Create the uploads directory and set ownership for the web server user
RUN mkdir -p uploads && chown -R www-data:www-data /var/www/html/uploads

# Set permissions for the index file
RUN chmod 444 /var/www/html/index.php

# Expose port 80
EXPOSE 80
