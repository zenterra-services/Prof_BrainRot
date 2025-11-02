# Railway Deployment Dockerfile for ProfBrainRot
FROM n8nio/n8n:latest

# Switch to root to install additional packages
USER root

# Install PostgreSQL client for database operations
RUN apt-get update && apt-get install -y postgresql-client curl && rm -rf /var/lib/apt/lists/*

# Create directory for workflows
RUN mkdir -p /workflows

# Copy workflows from repository
COPY n8n/workflows/ /workflows/

# Set proper ownership
RUN chown -R node:node /workflows

# Switch back to node user (as per n8n image)
USER node

# Set Railway-specific environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV N8N_HOST=0.0.0.0
ENV DB_TYPE=postgresdb

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5678/health || exit 1

# The n8n image will handle startup automatically - no need for custom start script