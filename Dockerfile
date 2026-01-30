# Use an official lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /

# Install system dependencies (add others if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Remove cache and copy application code
CMD rmdir src/__pycache__
COPY . .

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Default command (change if needed)
CMD ["python3", "src/app.py"]

# docker build -t istattracker .
# docker run -d -p 8080:8080 istattracker:latest