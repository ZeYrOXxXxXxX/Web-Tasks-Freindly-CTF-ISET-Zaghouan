FROM php:7.4-apache

# Install dependencies
# Added 'tcl-expect-dev' which provides expect_tcl.h
RUN apt-get update && apt-get install -y \
    tcl8.6-dev \
    expect \
    expect-dev \
    tcl-expect-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Expect extension
# CFLAGS points to where Debian installs Tcl/Expect headers
RUN CFLAGS="-I/usr/include/tcl8.6" pecl install expect && \
    docker-php-ext-enable expect

# Configure PHP
RUN echo "allow_url_include = On" >> /usr/local/etc/php/conf.d/security.ini \
    && echo "allow_url_fopen = On" >> /usr/local/etc/php/conf.d/security.ini

# Copy application files
COPY src/ /var/www/html/

# Create flag
RUN echo "Securinets{Exp3ct_Th3_Un3xp3ct3d_RCE_Wr4pp3r}" > /flag.txt

# Set permissions
RUN chown -R root:www-data /var/www/html && \
    chmod -R 755 /var/www/html && \
    chmod 444 /flag.txt

RUN a2enmod rewrite

EXPOSE 80