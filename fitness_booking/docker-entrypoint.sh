#!/bin/bash

set -e

postgres_ready() {
    python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

until postgres_ready; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done
echo "PostgreSQL is available"

echo "Applying database migrations..."
python manage.py migrate

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting uWSGI server..."
exec uwsgi --http "0.0.0.0:8000" \
           --module "fitness_booking.wsgi" \
           --master \
           --processes 4 \
           --threads 2 \
           --static-map /static=/app/staticfiles \
           --static-map /media=/app/media \
           --harakiri 30 \
           --max-requests 5000 \
           --vacuum