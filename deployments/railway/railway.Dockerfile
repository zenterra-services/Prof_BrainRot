# Railway Deployment Dockerfile for ProfBrainRot
FROM n8nio/n8n:latest

# Install PostgreSQL client for database operations
RUN apt-get update && apt-get install -y postgresql-client curl && rm -rf /var/lib/apt/lists/*

# Create directory for workflows
RUN mkdir -p /workflows

# Copy workflows from repository
COPY n8n/workflows/ /workflows/

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Ensure n8n is properly linked
RUN ln -sf $(which n8n) /usr/local/bin/n8n || true

# Set Railway-specific environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV N8N_HOST=0.0.0.0
ENV DB_TYPE=postgresdb

# Railway will inject these via environment variables:
# - N8N_BASIC_AUTH_USER
# - N8N_BASIC_AUTH_PASSWORD
# - N8N_ENCRYPTION_KEY
# - DB_POSTGRESDB_HOST (Railway's managed PostgreSQL)
# - DB_POSTGRESDB_PORT
# - DB_POSTGRESDB_DATABASE
# - DB_POSTGRESDB_USER
# - DB_POSTGRESDB_PASSWORD
# - OPENAI_API_KEY
# - WAN25_API_KEY
# - PROCESSING_NOTIFICATION_EMAIL

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5678/health || exit 1

# Start n8n using start script
CMD ["/start.sh"]