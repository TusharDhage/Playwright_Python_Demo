# Base image — Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching — faster rebuilds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers inside container
RUN playwright install --with-deps chromium

# Copy entire project into container
COPY . .

# Create reports directory
RUN mkdir -p reports/screenshots

# Default command — run smoke tests
CMD ["pytest", "tests/", "-m", "smoke", "--html=reports/report.html", "--self-contained-html", "-v"]