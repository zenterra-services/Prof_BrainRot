# Debug Dockerfile for Railway n8n deployment
FROM node:18-alpine

# Install dependencies
RUN apk add --no-cache postgresql-client curl bash

WORKDIR /app

# Create n8n user with different IDs to avoid conflicts
RUN addgroup -g 1001 -S n8n && \
    adduser -u 1001 -S n8n -G n8n

# Install n8n globally with verbose output
RUN npm install -g n8n --verbose

# Create workflows directory
RUN mkdir -p /workflows && \
    chown -R n8n:n8n /workflows

# Copy entrypoint script and workflows
COPY n8n/entrypoint.sh /entrypoint.sh
COPY n8n/workflows/ /workflows/

# Switch to n8n user
USER n8n

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV N8N_HOST=0.0.0.0
ENV DB_TYPE=postgresdb
ENV NODE_ENV=production

# Add debug startup script with timestamp to force rebuild
RUN echo "# Debug script created at $(date)" && \
    echo '#!/bin/bash
echo "==========================================="
echo "Debug: Starting n8n diagnostic..."
echo "Debug: Current time: $(date)"
echo "Debug: PATH=$PATH"
echo "Debug: which n8n=$(which n8n || echo "not found")"
echo "Debug: ls -la /usr/local/bin/n8n=$(ls -la /usr/local/bin/n8n 2>/dev/null || echo "not found")"
echo "Debug: Current user: $(whoami)"
echo "Debug: Working directory: $(pwd)"
echo "Debug: Environment variables:"
env | grep -E "(N8N|NODE)" || echo "No N8N/NODE env vars found"
echo "==========================================="
echo "Debug: Starting n8n..."
exec /usr/local/bin/n8n start' > /start-debug.sh && \
    chmod +x /start-debug.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5678/health || exit 1

EXPOSE 5678

# Use enhanced entrypoint script
ENTRYPOINT ["/entrypoint.sh"]