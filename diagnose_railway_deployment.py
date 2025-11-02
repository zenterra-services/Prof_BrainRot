#!/usr/bin/env python3
"""
Diagnostic script for Railway n8n deployment issues
"""

import subprocess
import sys
import os

def test_dockerfile_build():
    """Test if our Dockerfile builds and runs locally"""
    print("🧪 Testing Dockerfile build locally...")

    try:
        # Build the Docker image
        result = subprocess.run([
            'docker', 'build', '-f', 'Dockerfile', '-t', 'n8n-railway-test', '.'
        ], capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print("✅ Docker image built successfully")
            return True
        else:
            print(f"❌ Docker build failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Docker build timed out")
        return False
    except FileNotFoundError:
        print("⚠️  Docker not available for local testing")
        return False

def analyze_common_issues():
    """Analyze common n8n startup issues"""
    print("\n🔍 Analyzing common n8n startup issues...")

    issues = []

    # Check if n8n is properly installed in the Dockerfile
    with open('Dockerfile', 'r') as f:
        dockerfile_content = f.read()

    if 'npm install -g n8n' not in dockerfile_content:
        issues.append("n8n not explicitly installed via npm")

    if 'EXPOSE 5678' not in dockerfile_content:
        issues.append("Port 5678 not exposed")

    if '/usr/local/bin/n8n start' not in dockerfile_content:
        issues.append("n8n start command not found or incorrect path")

    # Check railway configuration
    try:
        with open('railway.json', 'r') as f:
            railway_config = f.read()

        if '5678' not in railway_config:
            issues.append("Port 5678 not configured in railway.json")

        if '/health' not in railway_config:
            issues.append("Health check endpoint not configured")

    except FileNotFoundError:
        issues.append("railway.json not found")

    return issues

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("\n💡 Suggested fixes:")

    fixes = [
        "1. Ensure n8n is installed globally with explicit path",
        "2. Verify port 5678 is exposed and accessible",
        "3. Check that health check endpoint /health is available",
        "4. Add environment variables for basic configuration",
        "5. Consider adding a startup delay or retry logic",
        "6. Add logging to debug startup issues"
    ]

    for fix in fixes:
        print(fix)

def create_debug_dockerfile():
    """Create a debug version of the Dockerfile with more logging"""
    debug_content = '''# Debug Dockerfile for Railway n8n deployment
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

# Copy workflows
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

# Add debug startup script
RUN echo '#!/bin/bash\\necho "Debug: Starting n8n diagnostic..."\\necho "Debug: PATH=$PATH"\\necho "Debug: which n8n=$(which n8n || echo \"not found\")"\\necho "Debug: ls -la /usr/local/bin/n8n=$(ls -la /usr/local/bin/n8n 2>/dev/null || echo \"not found\")"\\necho "Debug: Starting n8n..."\\nexec /usr/local/bin/n8n start' > /start-debug.sh && \
    chmod +x /start-debug.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5678/health || exit 1

EXPOSE 5678

# Use debug startup script
CMD ["/start-debug.sh"]
'''

    with open('Dockerfile.debug', 'w') as f:
        f.write(debug_content)

    print("\n📝 Created Dockerfile.debug with enhanced logging")

def main():
    """Main diagnostic function"""
    print("🔍 Railway n8n Deployment Diagnostic Tool")
    print("=" * 50)

    # Test local build
    docker_test = test_dockerfile_build()

    # Analyze common issues
    issues = analyze_common_issues()

    if issues:
        print(f"\n⚠️  Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ No obvious configuration issues found")

    # Suggest fixes
    suggest_fixes()

    # Create debug Dockerfile
    create_debug_dockerfile()

    print("\n🎯 Next steps:")
    print("1. Try building with Dockerfile.debug for more detailed logs")
    print("2. Check Railway environment variables")
    print("3. Monitor Railway deployment logs for specific error messages")
    print("4. Consider adding basic auth and database configuration")

if __name__ == "__main__":
    main()