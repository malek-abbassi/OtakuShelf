# Use the official uv image as builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set work directory
WORKDIR /app

# Copy dependency files
COPY . /app

# Install dependencies
RUN uv sync --frozen --no-cache

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV ENVIRONMENT=production

# Expose port
EXPOSE 8000

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
