#!/usr/bin/env bash
#!/bin/sh

apt-get update && apt-get install -y netcat

echo "Waiting for postgres..."

# Wait for postgres
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Collecting static..."
python manage.py collectstatic --no-input
echo "Static collecting finished"
python manage.py migrate

echo "Start gunicorn"
gunicorn -b 0.0.0.0:8000 watch_dog.wsgi --reload
exec "$@"
