#!/bin/bash
# Start script for ProfBrainRot on Railway

echo "🚀 Starting ProfBrainRot system..."

# Set up environment for n8n
export NODE_ENV=production

# Check if we're in the n8n Docker container
if [ -f "/usr/local/bin/n8n" ]; then
    echo "Starting n8n from Docker container..."
    exec /usr/local/bin/n8n start
else
    echo "Starting n8n..."
    # Try to find and run n8n
    exec n8n start
fi