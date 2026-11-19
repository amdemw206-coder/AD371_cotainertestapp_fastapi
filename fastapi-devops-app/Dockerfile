# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install necessary build tools for compiling dependencies if needed
RUN apk add --no-cache gcc libffi-dev musl-dev

# COPY ONLY dependency manifest first to leverage Docker layer caching
COPY requirements.txt .

# Install python dependencies into a local user directory
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Runtime Production Image
# ==========================================
FROM python:3.11-alpine AS runner

WORKDIR /app

# Security Best Practice: Create a non-privileged system group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy pre-installed python packages from the builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code AFTER dependencies (optimizes rebuild caching)
COPY main.py .

# Update environment paths for the non-root user
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch context to the non-root user
USER appuser

# Expose container port
EXPOSE 8000

# Container Health Check instruction
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).read()" || exit 1

# Start the application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]