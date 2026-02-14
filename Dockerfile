FROM python:3.12-slim

WORKDIR /app

# Copy project files
COPY . .

# Install all dependencies (including the local protocol package)
RUN pip install --no-cache-dir -e .
