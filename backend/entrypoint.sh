#!/bin/sh
set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec python -m uvicorn main:app --host 0.0.0.0 --port 8000