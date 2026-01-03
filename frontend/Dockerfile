FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy frontend application files
COPY frontend/server.py .
COPY frontend/templates/ templates/
COPY frontend/static/ static/

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Environment variables
ENV ENVIRONMENT=production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000', timeout=5)" || exit 1

# Run with Gunicorn in production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "60", "--access-logfile", "-", "server:app"]
