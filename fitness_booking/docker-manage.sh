#!/bin/bash

show_usage() {
  echo "Usage: $0 [OPTION]"
  echo ""
  echo "Options:"
  echo "  start-dev     Start development environment (with hot-reload)"
  echo "  start-prod    Start production environment"
  echo "  stop          Stop running containers"
  echo "  restart       Restart containers"
  echo "  logs          View logs from containers"
  echo "  migrate       Run Django migrations"
  echo "  collectstatic Collect static files"
  echo "  createsuperuser Create a Django superuser"
  echo "  shell         Run Django shell"
  echo "  test          Run Django tests"
  echo "  clean         Remove all containers, volumes, and images"
  echo "  build         Rebuild all Docker images"
  echo "  backup        Backup PostgreSQL database"
  echo "  restore       Restore PostgreSQL database"
  echo "  help          Show this help message"
  echo ""
}

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

run_django_command() {
  docker-compose exec web python manage.py "$@"
}

handle_error() {
  echo "Error: $1"
  exit 1
}

start_dev() {
  echo "Starting development environment..."
  docker-compose -f docker-compose-dev.yml up -d || handle_error "Failed to start development environment"
  echo "Development environment started. Access the application at: http://localhost:8060"
  echo "PGAdmin is available at: http://localhost:5050"
  echo "MailHog is available at: http://localhost:8025"
}

start_prod() {
  echo "Starting production environment..."
  docker-compose up -d || handle_error "Failed to start production environment"
  echo "Production environment started."
}

stop() {
  echo "Stopping containers..."
  docker-compose down || handle_error "Failed to stop containers"
  echo "Containers stopped."
}

restart() {
  stop
  if [ "$1" == "dev" ]; then
    start_dev
  else
    start_prod
  fi
}

logs() {
  docker-compose logs -f "$@"
}

migrate() {
  echo "Running migrations..."
  run_django_command migrate "$@" || handle_error "Failed to run migrations"
  echo "Migrations completed."
}

collectstatic() {
  echo "Collecting static files..."
  run_django_command collectstatic --noinput || handle_error "Failed to collect static files"
  echo "Static files collected."
}

createsuperuser() {
  echo "Creating superuser..."
  run_django_command createsuperuser || handle_error "Failed to create superuser"
  echo "Superuser created."
}

shell() {
  run_django_command shell
}

test() {
  echo "Running tests..."
  run_django_command test "$@" || handle_error "Tests failed"
  echo "Tests completed."
}

clean() {
  echo "This will remove all containers, volumes, and images. Are you sure? (y/n)"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Removing containers, volumes, and images..."
    docker-compose down -v
    docker rmi $(docker images -q -f "reference=fitness_booking*") 2>/dev/null || true
    echo "Cleanup completed."
  else
    echo "Cleanup cancelled."
  fi
}

build() {
  echo "Rebuilding Docker images..."
  if [ "$1" == "dev" ]; then
    docker-compose -f docker-compose-dev.yml build || handle_error "Failed to rebuild development images"
  else
    docker-compose build || handle_error "Failed to rebuild production images"
  fi
  echo "Docker images rebuilt."
}

backup() {
  BACKUP_FILE="fitness_booking_$(date +%Y%m%d_%H%M%S).sql"
  echo "Backing up PostgreSQL database to $BACKUP_FILE..."
  docker-compose exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" > "backups/$BACKUP_FILE" || \
    handle_error "Failed to backup database"
  echo "Database backup completed."
}

restore() {
  if [ -z "$1" ]; then
    echo "Please provide a backup file path"
    echo "Usage: $0 restore <backup_file>"
    exit 1
  fi
  
  BACKUP_FILE="$1"
  if [ ! -f "$BACKUP_FILE" ]; then
    handle_error "Backup file not found: $BACKUP_FILE"
  fi
  
  echo "Restoring PostgreSQL database from $BACKUP_FILE..."
  echo "This will overwrite your current database. Are you sure? (y/n)"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE" || \
      handle_error "Failed to restore database"
    echo "Database restore completed."
  else
    echo "Database restore cancelled."
  fi
}

mkdir -p backups

case "$1" in
  start-dev)
    start_dev
    ;;
  start-prod)
    start_prod
    ;;
  stop)
    stop
    ;;
  restart)
    restart "${@:2}"
    ;;
  logs)
    logs "${@:2}"
    ;;
  migrate)
    migrate "${@:2}"
    ;;
  collectstatic)
    collectstatic
    ;;
  createsuperuser)
    createsuperuser
    ;;
  shell)
    shell
    ;;
  test)
    test "${@:2}"
    ;;
  clean)
    clean
    ;;
  build)
    build "${@:2}"
    ;;
  backup)
    backup
    ;;
  restore)
    restore "$2"
    ;;
  help|*)
    show_usage
    ;;
esac

exit 0