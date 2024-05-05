#!/bin/sh
echo "Starting Database Initialization..."

# Database initialization logic
DB_PATH="/app/your_database.db"  # Ensure path is correct
SCHEMA_PATH="/app/schema.sql"    # Ensure path is correct

echo "Checking if database exists..."
if [ ! -f "$DB_PATH" ]; then
    echo "Database not found, creating database schema..."
    sqlite3 $DB_PATH < $SCHEMA_PATH
else
    echo "Database already exists."
fi

echo "Database setup complete."

# Start Gunicorn with Flask application
echo "Starting Gunicorn..."
exec gunicorn -b :3000 -w 4 app:app
