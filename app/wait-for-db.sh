#!/bin/bash

# Wait for the database to be ready
echo "Waiting for the database to be ready..."

while ! nc -z mysql 3306; do
  sleep 1
done

echo "Database is ready. Starting the application."

exec "$@"
