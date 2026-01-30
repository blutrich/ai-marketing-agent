# Slack Bot with Video Rendering - Docker Image for Railway
FROM python:3.11-slim

# Install system dependencies including Chromium for Remotion
RUN apt-get update && apt-get install -y \
    curl \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (required for Remotion)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install video project dependencies
COPY video/package.json video/package-lock.json /app/video/
RUN cd /app/video && npm ci --production

# Copy video source files
COPY video/src/ /app/video/src/
COPY video/public/ /app/video/public/
COPY video/tsconfig.json /app/video/

# Copy Python requirements and install
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Slack bot code
COPY server/slack_bot.py /app/slack_bot.py

# Create output directory
RUN mkdir -p /app/video/out /app/video/src/temp

# Set environment variables for Docker mode
ENV DOCKER_ENV=1
ENV VIDEO_PROJECT_PATH=/app/video
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check (Slack bot doesn't have HTTP endpoint, just check process)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "python slack_bot.py" || exit 1

# Run the Slack bot
CMD ["python", "slack_bot.py"]
