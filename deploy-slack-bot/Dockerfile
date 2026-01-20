# Slack Bot for Marketing Agent
FROM python:3.11-slim

# Install process monitoring for healthcheck
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY slack_bot.py /app/slack_bot.py

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check - verify process is running (no HTTP endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "python slack_bot.py" || exit 1

CMD ["python", "slack_bot.py"]
