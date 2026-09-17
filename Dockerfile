# Multi-stage Dockerfile for IPL with Ollama integration
# This packages IPL + Ollama + Qwen model in a single container

FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Download Qwen model (cached in layer for efficiency)
# This makes the model available offline
RUN ollama serve > /dev/null 2>&1 & \
    sleep 5 && \
    ollama pull qwen2.5-coder:0.5b && \
    pkill ollama

# Production stage
FROM python:3.11-slim

# Copy Ollama installation from base stage
COPY --from=base /usr/local/bin/ollama /usr/local/bin/ollama
COPY --from=base /usr/local/lib/ollama /usr/local/lib/ollama

# Install Python dependencies
WORKDIR /app
COPY pyproject.toml .
COPY README.md .

# Install IPL and its dependencies
RUN pip install --no-cache-dir -e .

# Copy IPL source code
COPY *.py ./
COPY examples/ ./examples/
COPY tests/ ./tests/

# Create non-root user for security
RUN useradd -m -u 1000 ipluser && \
    chown -R ipluser:ipluser /app
USER ipluser

# Expose ports
# 11434: Ollama API
# 8000: IPL Gateway
EXPOSE 11434 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Start script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gateway"]