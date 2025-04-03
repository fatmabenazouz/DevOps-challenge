#!/bin/bash python3
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE fitness_booking;
    GRANT ALL PRIVILEGES ON DATABASE fitness_booking TO $POSTGRES_USER;
EOSQL

echo "PostgreSQL initialized with fitness_booking database"