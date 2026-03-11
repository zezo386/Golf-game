# Use Python 3.9 slim image as base
FROM python:3.9-slim as builder

WORKDIR /app

# First, upgrade pip and set timeout
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip config set global.timeout 100

COPY requirements.txt .
RUN pip download --no-cache-dir --dest /wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libsdl2-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /wheels /wheels
COPY requirements.txt .

# Install from local wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy the rest of the application
COPY ball.py main.py wall.py ./
COPY "my-mom-is-kinda-homeless.mp3" .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV DISPLAY=:0
CMD ["python", "main.py"]