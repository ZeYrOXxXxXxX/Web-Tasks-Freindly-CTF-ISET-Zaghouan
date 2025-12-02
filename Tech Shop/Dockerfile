FROM php:7.4-apache

# Install MySQLi
RUN docker-php-ext-install mysqli

# Copy flag
ARG FLAG_CONTENT
RUN echo "$FLAG_CONTENT" > /flag.txt && chmod 444 /flag.txt

# Copy web files
COPY html/ /var/www/html/

# Permissions
RUN chown -R root:root /var/www/html && \
    mkdir -p /var/www/html/images && \
    chown -R www-data:www-data /var/www/html/images && \
    chmod 755 /var/www/html/images

EXPOSE 80
