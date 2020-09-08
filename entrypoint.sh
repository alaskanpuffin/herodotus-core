#!/bin/bash

if [ ! -f /app/data/db.sqlite3 ]; then
    echo "Applying initial database migrations"
    python manage.py migrate
    echo "Adding Default Admin User"
    export DJANGO_SUPERUSER_PASSWORD=admin
    python manage.py createsuperuser --noinput --username admin --email example@example.com 
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn herodotus.wsgi