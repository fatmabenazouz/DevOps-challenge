# Docker Setup for Fitness Class Booking System

This document provides instructions for setting up and running the Fitness Class Booking System using Docker.

## Prerequisites

- Docker Engine (version 20.10.0 or later)
- Docker Compose (version 2.0.0 or later)
- Git

## Quick Start

### Development Environment

To start the application in development mode with hot-reloading:

```bash
# Clone the repository (if not already done)
git clone 
cd fitness-booking

# Copy the environment file template
cp .env.docker .env

# Generate a secure secret key and update it in your .env file
python scripts/generate_secret_key.py

# Start the development environment
./docker-manage.sh start-dev
```

The development environment will be available at:
- Django application: [http://localhost:8000](http://localhost:8000)
- PGAdmin: [http://localhost:5050](http://localhost:5050)
- MailHog (for email testing): [http://localhost:8025](http://localhost:8025)

Default admin credentials (in development):
- Username: admin
- Password: adminpassword
- Email: admin@example.com

### Production Environment

To start the application in production mode:

```bash
# Clone the repository
git clone 
cd fitness-booking

# Copy the environment file template
cp .env.docker .env

# Modify the .env file with your production settings
# Generate a secure secret key and update it in your .env file
python scripts/generate_secret_key.py

# Start the production environment
./docker-manage.sh start-prod
```

## Docker Management Script

We provide a convenient script to manage Docker operations: `docker-manage.sh`

Usage:
```bash
./docker-manage.sh [OPTION]
```

Available options:
- `start-dev`: Start development environment (with hot-reload)
- `start-prod`: Start production environment
- `stop`: Stop running containers
- `restart`: Restart containers
- `logs`: View logs from containers
- `migrate`: Run Django migrations
- `collectstatic`: Collect static files
- `createsuperuser`: Create a Django superuser
- `shell`: Run Django shell
- `test`: Run Django tests
- `clean`: Remove all containers, volumes, and images
- `build`: Rebuild all Docker images
- `backup`: Backup PostgreSQL database
- `restore`: Restore PostgreSQL database
- `help`: Show help message

## Available Services

The Docker setup includes the following services:

1. **web**: Django application with uWSGI
2. **db**: PostgreSQL database
3. **nginx**: Nginx web server (default for production)
4. **certbot**: SSL certificate management for Nginx
5. **pgadmin**: PostgreSQL admin interface (development only)
6. **mailhog**: Email testing tool (development only)

In the `docker-compose.yml` file, there's also a commented-out configuration for Caddy as an alternative to Nginx.

## Environment Variables

The application uses the following environment variables which should be set in your `.env` file:

### Django Settings
- `SECRET_KEY`: Django secret key (use the generate_secret_key.py script)
- `DEBUG`: Set to 'True' for development, 'False' for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Settings
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (set to 'db' for Docker)
- `DB_PORT`: Database port (default: 5432)

### Email Settings
- `SENDGRID_API_KEY`: SendGrid API key for sending emails
- `DEFAULT_FROM_EMAIL`: Default sender email address

### Port Configuration
- `NGINX_HTTP_PORT`: HTTP port for Nginx (default: 80)
- `NGINX_HTTPS_PORT`: HTTPS port for Nginx (default: 443)
- `CADDY_HTTP_PORT`: HTTP port for Caddy (default: 80)
- `CADDY_HTTPS_PORT`: HTTPS port for Caddy (default: 443)

## Directory Structure

- `docker/`: Container-specific files
  - `postgres/`: PostgreSQL Docker files
  - `nginx/`: Nginx Docker files
  - `caddy/`: Caddy Docker files
- `scripts/`: Utility scripts
- `backups/`: Database backups

## SSL Certificates

In the production environment, the Nginx configuration is set up to use SSL certificates provided by Certbot.

To initialize SSL certificates:

```bash
# First start the containers
docker-compose up -d

# Run Certbot to obtain certificates
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot \
  -d your-domain.com -d www.your-domain.com

# Restart Nginx to apply the certificates
docker-compose restart nginx
```

## Switching Between Nginx and Caddy

The default setup uses Nginx as the web server. To use Caddy instead:

1. Open `docker-compose.yml`
2. Comment out the `nginx` and `certbot` services
3. Uncomment the `caddy` service
4. Update the volume definitions at the bottom of the file
5. Restart the containers with `./docker-manage.sh restart`

## Backup and Restore

To backup your database:
```bash
./docker-manage.sh backup
```

To restore from a backup:
```bash
./docker-manage.sh restore backups/your-backup-file.sql
```

## Troubleshooting

### Checking Logs
```bash
# All services
./docker-manage.sh logs

# Specific service
./docker-manage.sh logs web
./docker-manage.sh logs db
./docker-manage.sh logs nginx
```

### Common Issues

1. **Permission Issues**: If you encounter permission issues with volume mounts, you may need to adjust the file permissions on your host:
   ```bash
   sudo chown -R $USER:$USER .
   ```

2. **Port Conflicts**: If a service cannot start due to port conflicts, check if another process is using the same port or modify the port mappings in your `.env` file.

3. **Database Connection Issues**: If the web application cannot connect to the database, ensure the database service is running and the correct environment variables are set.