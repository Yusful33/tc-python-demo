# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pip, dependencies, and pytest
RUN python -m ensurepip --upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Docker CLI to use Testcontainers
RUN apt-get update && \
    apt-get install -y docker.io

# Default command to run pytest
CMD ["pytest", "tests/test_customers.py"]
