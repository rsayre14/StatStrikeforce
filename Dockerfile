# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Ensure gunicorn is installed
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

# Make sure the initialization script is executable
COPY init_db.sh /app/
RUN chmod +x /app/init_db.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set ENTRYPOINT to use the initialization script
ENTRYPOINT ["/app/init_db.sh"]
