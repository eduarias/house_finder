#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput
echo "Complete collecting static files"

# Apply database migrations
sleep 5
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000