# Railway Deployment Dockerfile for ProfBrainRot - Simplified Approach
FROM node:18-alpine

# Install PostgreSQL client and other dependencies
RUN apk add --no-cache postgresql-client curl bash

# Create app directory
WORKDIR /app

# Create n8n user and group with different IDs
RUN addgroup -g 1001 -S n8n && \
    adduser -u 1001 -S n8n -G n8n

# Install n8n globally
RUN npm install -g n8n

# Create workflows directory
RUN mkdir -p /workflows && \
    chown -R n8n:n8n /workflows

# Copy workflows
COPY n8n/workflows/ /workflows/

# Set proper permissions
RUN chown -R n8n:n8n /workflows

# Switch to n8n user
USER n8n

# Set Railway-specific environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV N8N_HOST=0.0.0.0
ENV DB_TYPE=postgresdb
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5678/health || exit 1

# Expose port
EXPOSE 5678

# Start n8n with explicit path
CMD ["/usr/local/bin/n8n", "start"]