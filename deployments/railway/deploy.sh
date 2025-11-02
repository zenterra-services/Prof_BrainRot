#!/bin/bash
# Railway Deployment Script for ProfBrainRot

echo "🚂 Starting Railway deployment for ProfBrainRot..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Create new project (optional - you can also use existing project)
echo "📦 Creating Railway project..."
railway init --name profbrainrot --template docker

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set \
    N8N_BASIC_AUTH_USER=admin \
    N8N_BASIC_AUTH_PASSWORD=your-secure-password \
    N8N_ENCRYPTION_KEY=your-32-character-encryption-key \
    OPENAI_API_KEY=your-openai-api-key \
    WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856 \
    PROCESSING_NOTIFICATION_EMAIL=your-email@example.com

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

# Get deployment URL
echo "📍 Getting deployment URL..."
DEPLOYMENT_URL=$(railway status | grep -o 'https://[^[:space:]]*' | head -1)

echo "🎉 Deployment complete!"
echo "Access your n8n dashboard at: $DEPLOYMENT_URL"
echo "Railway Dashboard: https://railway.app/project/$(railway status | grep -o 'Project: [^[:space:]]*' | cut -d' ' -f2)"

echo ""
echo "Next steps:"
echo "1. Access n8n at: $DEPLOYMENT_URL"
echo "2. Import workflows from /n8n/workflows/"
echo "3. Configure credentials in n8n"
echo "4. Test with a lesson plan"
echo "5. Monitor usage in Railway dashboard"""}