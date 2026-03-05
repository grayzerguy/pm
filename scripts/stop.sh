#!/bin/bash
CONTAINER_NAME=pmapp

docker rm -f "$CONTAINER_NAME" || true
