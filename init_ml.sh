#!/bin/sh

# Start Gunicorn with Flask application
exec gunicorn -b :3001 -w 4 app:app
