FROM python:3.12-slim

WORKDIR /app

# System deps: supervisor + nginx + Node.js (for frontend build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    nginx \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies (including the local protocol package)
RUN pip install --no-cache-dir -e .

# Build React frontend — output lands in ui/frontend/dist/
RUN cd ui/frontend && npm ci && npm run build

# Place supervisor and nginx configs in their system locations
COPY supervisord.conf /etc/supervisor/conf.d/news-brief.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/news-brief.conf"]
