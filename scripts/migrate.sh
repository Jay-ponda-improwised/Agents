#!/bin/bash
# Migration script for PostgreSQL database

set -e

echo "Starting database migrations..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "PostgreSQL is ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
conda run -n langchain_env python -m alembic upgrade head

echo "Database migrations completed successfully!"

# Exit with success status
exit 0