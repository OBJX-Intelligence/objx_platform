# OBJX Intelligence Platform - Dockerfile
# Author: Manus AI
# Date: July 25, 2025
# Version: 1.0 - Production Ready

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_deployment.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_deployment.txt

# Copy application files
COPY objx_deployment_app.py app.py
COPY dashboard_*.html ./
COPY static/ ./static/
COPY templates/ ./templates/
COPY *.svg ./static/

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Create non-root user
RUN useradd -m -u 1000 objx && chown -R objx:objx /app
USER objx

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]

