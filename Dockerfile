# --- Stage 1: Build Frontend ---
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build the frontend
RUN npm run build

# --- Stage 2: Final Production Image ---
FROM python:3.12-slim

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set Work Directory
WORKDIR /app

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it script
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# Copy Backend Application Code
COPY ./src /app/src

# Copy Built Frontend from Builder Stage
COPY --from=builder /app/frontend/build /app/frontend/build

# Expose Port
EXPOSE 8000

# Run Application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
