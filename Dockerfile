# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pip, dependencies, and pytest
RUN python -m ensurepip --upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Docker CLI to use Testcontainers
RUN apt-get update && \
    apt-get install -y docker.io

# Copy the entry point script
COPY entrypoint.sh /entrypoint.sh

# Make the entry point script executable
RUN chmod +x /entrypoint.sh

# Set the entry point script
ENTRYPOINT ["/entrypoint.sh"]

# Keep the container running indefinitely
CMD ["tail", "-f", "/dev/null"]
