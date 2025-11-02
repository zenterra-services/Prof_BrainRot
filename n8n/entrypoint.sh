#!/bin/bash
# Enhanced n8n entrypoint for Railway deployment

echo "==========================================="
echo "Railway n8n Enhanced Startup Diagnostic"
echo "==========================================="
echo "Time: $(date)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"
echo "PATH: $PATH"
echo ""

# Check if n8n binary exists
echo "Checking n8n binary..."
if [ -f "/usr/local/bin/n8n" ]; then
    echo "✅ n8n binary found at /usr/local/bin/n8n"
    ls -la /usr/local/bin/n8n
else
    echo "❌ n8n binary NOT found at /usr/local/bin/n8n"
    echo "Searching for n8n..."
    find /usr -name "n8n" 2>/dev/null || echo "n8n not found in /usr"
    which n8n || echo "n8n not in PATH"
fi

echo ""
echo "Environment variables:"
env | grep -E "(N8N|NODE|PORT)" || echo "No relevant env vars found"

echo ""
echo "Network configuration:"
echo "Port: ${N8N_PORT:-5678}"
echo "Host: ${N8N_HOST:-0.0.0.0}"

echo ""
echo "Trying to start n8n..."

# Try different ways to start n8n
if [ -f "/usr/local/bin/n8n" ]; then
    echo "Starting n8n with explicit path..."
    exec /usr/local/bin/n8n start
elif command -v n8n >/dev/null 2>&1; then
    echo "Starting n8n from PATH..."
    exec n8n start
else
    echo "❌ Cannot find n8n binary!"
    echo "Available node binaries:"
    ls -la /usr/local/bin/ | grep -E "(node|npm|n8n)" || echo "No node-related binaries found"
    echo "Exiting with error..."
    exit 1
fi