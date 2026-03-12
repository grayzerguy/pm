#!/bin/bash
set -e

IMAGE_NAME=pmapp
CONTAINER_NAME=pmapp

# build image
docker build -t "$IMAGE_NAME" .

# remove existing container if any
if docker ps -a --format '{{.Names}}' | grep -Eq "^$CONTAINER_NAME$"; then
    docker rm -f "$CONTAINER_NAME" || true
fi

# run container, passing .env from project root if it exists
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"
ENV_ARG=""
if [ -f "$ENV_FILE" ]; then
    ENV_ARG="--env-file $ENV_FILE"
fi

docker run -d --name "$CONTAINER_NAME" -p 8000:8000 $ENV_ARG "$IMAGE_NAME"

echo "Container started, access http://localhost:8000"