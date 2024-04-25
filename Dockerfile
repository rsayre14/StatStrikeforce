# Use an appropriate base image that supports serving static files
FROM nginx:latest

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy all the necessary files to the container
COPY index.html .
COPY cover.css .
COPY background.jpeg .
COPY menuswap.js .
COPY formHandler.js .
