# GitHub Actions CI/CD Pipeline

This document explains the Continuous Integration and Continuous Deployment (CI/CD) pipeline set up using GitHub Actions for the Fitness Class Booking System.

## Pipeline Overview

The CI/CD pipeline automates the following tasks:

1. **Code Quality Assessment (Linting)**
   - Checks code syntax with Flake8
   - Verifies code formatting with Black
   - Ensures proper import sorting with isort

2. **Testing**
   - Runs unit tests and integration tests
   - Generates coverage reports
   - Uses a PostgreSQL service container for database testing

3. **Docker Image Building**
   - Builds Docker images for:
     - Django application
     - PostgreSQL database
     - Nginx web server
   - Runs only on pushes to main/master branches

4. **Docker Hub Publishing**
   - Pushes successfully built Docker images to Docker Hub
   - Tags images with branch name, commit SHA, and 'latest'

## Workflow File

The workflow is defined in `.github/workflows/main.yml` and is triggered on:
- Pushes to `main`, `master`, or `develop` branches
- Pull requests targeting these branches

## Prerequisites

To use this workflow, you need to set up the following secrets in your GitHub repository:

1. `DOCKERHUB_USERNAME`: Your Docker Hub username
2. `DOCKERHUB_TOKEN`: A Docker Hub access token (not your password)

### Setting up GitHub Secrets

1. Navigate to your GitHub repository
2. Go to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add the two secrets mentioned above

## Docker Hub Token Creation

To create a Docker Hub access token:

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to your account settings (click on your username)
3. Navigate to Security > New Access Token
4. Give the token a descriptive name (e.g., "GitHub Actions")
5. Copy the generated token immediately (it won't be shown again)
6. Use this token as your `DOCKERHUB_TOKEN` secret

## How It Works

### Code Quality Job (`lint`)

This job:
- Sets up a Python environment
- Installs code quality tools (flake8, black, isort)
- Checks your code against style guidelines
- Always runs on all pushes and pull requests

### Tests Job (`test`)

This job:
- Depends on the successful completion of the `lint` job
- Sets up a PostgreSQL service container
- Runs database migrations
- Executes tests and generates coverage reports
- Always runs on all pushes and pull requests

### Build and Push Jobs (`build`, `build-postgres`, `build-nginx`)

These jobs:
- Depend on the successful completion of the `test` job
- Only run on pushes to main/master branches (not on PRs)
- Build Docker images using caching for efficiency
- Tag images with multiple formats for traceability
- Push images to Docker Hub

## Local Testing

You can test most aspects of the workflow locally:

```bash
# Code quality
pip install flake8 black isort
flake8 .
black --check .
isort --check .

# Tests
python manage.py test
```

## Troubleshooting

If the workflow fails, check the following:

1. **Linting Issues**
   - Run linting tools locally to identify and fix issues
   - Consider adding an `.flake8` configuration file to customize rules

2. **Test Failures**
   - Check the GitHub Actions logs for specific test failures
   - Try reproducing the test environment locally

3. **Docker Build Failures**
   - Verify that your Dockerfiles are valid
   - Check that all required files are properly referenced in the Dockerfiles

4. **Docker Push Failures**
   - Ensure your Docker Hub credentials are correct
   - Verify that you have permission to push to the specified repositories

## Extending the Workflow

You can extend this workflow by:

1. Adding additional linting tools
2. Implementing security scanning of Docker images
3. Setting up automated deployment to staging/production environments
4. Adding notifications (Slack, email, etc.)
5. Incorporating performance testing

To modify the workflow, edit the `.github/workflows/main.yml` file.