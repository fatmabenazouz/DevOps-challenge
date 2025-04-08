# Fitness Class Booking System

A comprehensive Django application for fitness centers to manage class schedules and customer bookings with Docker containerization, CI/CD pipeline, and Ansible deployment.

## Features

- **User Authentication**: Registration, login, profile management
- **Class Management**: Browse fitness classes by category, instructor, or time
- **Booking System**: Book classes, view upcoming sessions, cancel bookings
- **Instructor Profiles**: View instructor details and their class schedules
- **Email Notifications**: Booking confirmations, reminders, cancellations
- **Feedback System**: Submit ratings and reviews for attended classes
- **Admin Dashboard**: Manage classes, instructors, bookings, and users

## Technology Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx/Caddy (configurable)
- **Email**: SendGrid API
- **CI/CD**: GitHub Actions
- **Deployment**: Ansible
- **Frontend**: Bootstrap 5, JavaScript

## Setup and Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fitness-booking.git
   cd fitness-booking
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Copy the environment template:
   ```bash
   cp .env.docker .env
   ```

5. Generate a secret key:
   ```bash
   python3 scripts/generate_secret_key.py
   ```

6. Update your .env file with the generated secret key and other settings

7. Run migrations:
   ```bash
   python3 manage.py migrate
   ```

8. Create a superuser:
   ```bash
   python3 manage.py createsuperuser
   ```

9. Run the development server:
   ```bash
   python3 manage.py runserver
   ```

### Docker Setup

1. Make sure Docker and Docker Compose are installed

2. Use the Docker management script to build and start the development environment:
   ```bash
   chmod +x docker-manage.sh
   ./docker-manage.sh build dev
   ./docker-manage.sh start-dev
   ```

3. The application will be available at:
   - Web application: http://localhost:8060
   - PGAdmin: http://localhost:5050
   - MailHog (for email testing): http://localhost:8025
   

## Continuous Integration and Deployment

### CI Pipeline

The project uses GitHub Actions for continuous integration:

- **Code Quality**: Linting with Flake8
- **Testing**: Running unit and integration tests
- **Docker Images**: Building and pushing to Docker Hub


### Deployment with Ansible

Automated deployment is handled by Ansible:

1. Configure your target server in the `ansible/inventory.yml` file
2. Set required environment variables or GitHub secrets
3. Run the deployment playbook:
   ```bash
   cd ansible
   ansible-playbook -i inventory.yml deploy.yml
   ```


## Running Tests

To run the test suite:

```bash
python3 manage.py test
```

For more comprehensive testing with coverage reports:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Usage Guide

### Admin Access

1. Access the admin interface at `/admin/`
2. Use your superuser credentials to log in
3. Manage users, classes, instructors, and bookings

### User Registration and Authentication

1. New users can register at `/accounts/register/`
2. Existing users can log in at `/accounts/login/`
3. Users can update their profile at `/accounts/profile/edit/`

### Booking a Class

1. Browse available classes at `/classes/`
2. Click on a class to view details
3. Select an available time slot
4. Confirm your booking

### Managing Bookings

1. View all bookings at `/bookings/`
2. Cancel bookings if needed
3. Submit feedback for attended classes


## Developed by

- Fatma Ben Azouz