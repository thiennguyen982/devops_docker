# Use the official Drupal 8.6 image as base
FROM drupal:latest

# Install git and cleanup after apt install
RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Change working directory to Drupal themes directory
WORKDIR /var/www/html/themes

# Clone the Bootstrap theme from Drupal.org and change permissions
RUN git clone --branch 8.x-3.x --single-branch --depth 1 https://git.drupal.org/project/bootstrap.git \
    && chown -R www-data:www-data bootstrap \
    && rm -rf /var/lib/apt/lists/*

#Expose port80
EXPOSE 80

# Change working directory back to Drupal default
WORKDIR /var/www/html
