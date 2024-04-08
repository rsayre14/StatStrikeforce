#!/bin/sh

# Database initialization logic
DB_PATH="./your_database.db"
SCHEMA_PATH="./schema.sql"

if [ ! -f "$DB_PATH" ]; then
    echo "Creating database schema..."
    sqlite3 $DB_PATH < $SCHEMA_PATH
fi

# Start Gunicorn with Flask application
exec gunicorn -b :5000 -w 4 app:app
