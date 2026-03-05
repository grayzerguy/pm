# syntax=docker/dockerfile:1

# first stage: build the Next.js frontend (requires Node >=20 for Next 16)
FROM node:20-alpine as frontend
WORKDIR /app/frontend

# copy only package definitions first for faster rebuilds
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --silent

# copy entire frontend and build/export statically
COPY frontend/ .
RUN BUILD_EXPORT=1 npm run build

# second stage: python runtime with backend
FROM python:3.11-slim as base
WORKDIR /app

# install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy backend application
COPY backend/app ./app

# copy the exported static files from the frontend build stage
COPY --from=frontend /app/frontend/out ./static

ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
