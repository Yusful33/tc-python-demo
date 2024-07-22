#!/bin/bash

# Wait for Docker socket to be available
while (! docker stats --no-stream ); do
  echo "Waiting for Docker socket..."
  sleep 1
done

# Execute the command passed to the container
exec "$@"
