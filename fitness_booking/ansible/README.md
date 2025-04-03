# Ansible Deployment for Fitness Booking System

This directory contains Ansible playbooks and configurations for deploying the Fitness Booking System to production servers.

## Directory Structure

- `deploy.yml`: Main playbook for deploying the application
- `inventory.yml`: Inventory file defining server groups
- `templates/`: Jinja2 templates for configuration files
  - `docker-compose.yml.j2`: Template for docker-compose configuration
  - `.env.j2`: Template for environment variables

## Requirements

- Ansible 2.9+
- Target server with:
  - Ubuntu 20.04+ or Debian 11+
  - SSH access
  - sudo privileges

## Configuration

The deployment uses the following environment variables, which should be set in your CI/CD system (GitHub Actions):

- `TARGET_SERVER`: Hostname or IP of the target server
- `SSH_USER`: SSH username for the target server
- `SSH_PRIVATE_KEY`: SSH private key for authentication
- `DOCKER_HUB_USERNAME`: Docker Hub username for pulling images
- `DOCKER_HUB_TOKEN`: Docker Hub access token
- `DB_PASSWORD`: PostgreSQL database password
- `SECRET_KEY`: Django secret key
- `SENDGRID_API_KEY`: SendGrid API key for email functionality
- `APP_PORT`: Application port (defaults to 8000)
- `NGINX_HTTP_PORT`: HTTP port for Nginx (defaults to 80)
- `NGINX_HTTPS_PORT`: HTTPS port for Nginx (defaults to 443)

## Manual Deployment

If you need to run the deployment manually:

1. Set up the required environment variables:

```bash
export TARGET_SERVER=your-server-hostname-or-ip
export SSH_USER=your-ssh-username
export DOCKER_HUB_USERNAME=your-dockerhub-username
export DOCKER_HUB_TOKEN=your-dockerhub-token
export DB_PASSWORD=your-database-password
export SECRET_KEY=your-django-secret-key
export SENDGRID_API_KEY=your-sendgrid-api-key
export APP_PORT=8000
export NGINX_HTTP_PORT=80
export NGINX_HTTPS_PORT=443
```

2. Run the playbook:

```bash
ansible-playbook -i inventory.yml deploy.yml
```

## SSL Configuration

The deployment includes Certbot for SSL certificate management. Initially, self-signed certificates are used. To obtain proper SSL certificates:

1. SSH into your server
2. Run the following command:

```bash
docker-compose exec certbot certonly --webroot --webroot-path /var/www/certbot -d yourdomain.com -d www.yourdomain.com
```

3. Restart Nginx:

```bash
docker-compose restart nginx
```

## Troubleshooting

### Checking Logs

```bash
# View logs for the web application
docker-compose logs web

# View logs for Nginx
docker-compose logs nginx

# View logs for PostgreSQL
docker-compose logs db
```

### Common Issues

1. **Database Connection Issues**: Ensure the database password is correctly set in the environment variables
2. **Permission Errors**: Make sure the SSH user has proper permissions on the target directory
3. **Port Conflicts**: Check if the configured ports are already in use on the target server