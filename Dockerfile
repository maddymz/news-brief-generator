FROM python:3.12-slim

WORKDIR /app

# System deps: supervisor (process manager) + nginx (reverse proxy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install all dependencies (including the local protocol package)
RUN pip install --no-cache-dir -e .

# Copy supervisor and nginx configs
COPY supervisord.conf /etc/supervisor/conf.d/news-brief.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor

EXPOSE 80

# docker-compose.yml overrides CMD per-service — this is only used in Fly.io mode
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
