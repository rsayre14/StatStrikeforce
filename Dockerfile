# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Ensure gunicorn is installed
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

# Make sure the initialization script is executable
COPY init_ml.sh /app/
RUN chmod +x /app/init_ml.sh

# Make port 5000 available to the world outside this container
EXPOSE 3001

# Set ENTRYPOINT to use the initialization script
ENTRYPOINT ["/app/init_ml.sh"]
