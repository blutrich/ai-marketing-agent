# AI Marketing Content Generator - Docker Image for Railway
FROM python:3.11-slim

# Install system dependencies and Claude Code CLI
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Claude Code CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Set working directory
WORKDIR /app

# Copy brand data for skills that reference /app/brands/
COPY brands/ /app/brands/

# Copy skills directory from project root
# This is CRITICAL - skills must be at /app/.claude/skills/
COPY .claude/skills/ /app/.claude/skills/

# Copy server requirements and install dependencies
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy server application code
COPY server/main.py /app/main.py
COPY server/agent/ /app/agent/
COPY server/db/ /app/db/
COPY server/models/ /app/models/

# Create non-root user (required for Claude Code CLI bypassPermissions)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Environment variables
ENV PORT=8000
ENV SKILLS_DIR=/app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Switch to non-root user
USER appuser

# Run the server (use Railway's PORT env variable)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
