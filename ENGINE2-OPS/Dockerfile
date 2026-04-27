# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY main.py .
COPY ops/runner.py ./ops/
COPY src src/

# Install dependencies
RUN pip install --no-cache-dir sympy

# Production stage
FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir sympy

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy application code from builder
COPY --from=builder --chown=appuser:appuser /app .

# Create log directories
RUN mkdir -p logs state && chown -R appuser:appuser logs state

# Set user to non-root
USER appuser

# Health check
HEALTHCHECK --start-period=5s --retries=2 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default: show usage
CMD ["python", "main.py"]
