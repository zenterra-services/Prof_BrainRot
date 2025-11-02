# Railway Deployment Guide for ProfBrainRot

Step-by-step guide to deploy your ProfBrainRot system to Railway cloud platform.

## 🚀 Quick Start (5 minutes)

### Step 1: Prepare Your Code

1. **Ensure your code is ready:**
   ```bash
   cd Prof_BrainRot
   git status  # Make sure everything is committed
   ```

2. **Check your files are present:**
   ```
   Prof_BrainRot/
   ├── deployments/
   │   └── railway/
   │       ├── railway.Dockerfile
   │       ├── railway.json
   │       └── docker-compose.yml
   ├── n8n/
   │   └── workflows/
   │       ├── lesson_processor.json
   │       └── queue_processor_wan25.json
   ├── web/
   │   └── index.html
   ├── database/
   │   └── schema.sql
   └── README.md
   ```

### Step 2: Create Railway Account

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Verify your email

### Step 3: Connect Your Repository

**Option A: Using Railway Web Interface (Recommended)**

1. Click "New Project" → "Deploy from GitHub"
2. Select your ProfBrainRot repository
3. Authorize Railway to access your repo

**Option B: Using Railway CLI**

```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login to Railway
railway login

# Initialize Railway project
railway init --name profbrainrot --template docker
```

### Step 4: Configure Environment Variables

**Using Railway Web Interface:**

1. Go to your Railway project dashboard
2. Click on "Variables" tab
3. Add these environment variables:

```env
# Authentication
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-32-character-encryption-key

# API Keys
OPENAI_API_KEY=your-openai-api-key
WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856

# Notifications
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com

# Railway will provide these automatically:
# DATABASE_URL (managed PostgreSQL)
# RAILWAY_TCP_PROXY_DOMAIN
# RAILWAY_TCP_PROXY_PORT
```

### Step 5: Deploy Your Application

**Using Git (Recommended):**

```bash
# Add Railway files to git
git add deployments/railway/
git commit -m "Add Railway deployment configuration"

# Push to deploy
git push origin main
```

**Using Railway CLI:**

```bash
# Deploy directly
railway up
```

### Step 6: Monitor Deployment

1. **Watch deployment logs:**
   - Railway Dashboard → Your Project → Deployments
   - Look for "Build successful" and "Application started"

2. **Check deployment status:**
   ```bash
   railway status
   railway logs
   ```

### Step 7: Access Your Application

1. **Get your Railway URL:**
   - Railway will provide a URL like: `https://profbrainrot-production.up.railway.app`

2. **Access n8n dashboard:**
   - Open: `https://profbrainrot-production.up.railway.app`
   - Login with your configured username/password

3. **Test the system:**
   - Import workflows from `/n8n/workflows/`
   - Configure credentials in n8n
   - Test with a sample lesson plan

## 🔧 Advanced Configuration

### Custom Domain (Optional)

1. Railway Dashboard → Settings → Domains
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `profbrainrot.yourdomain.com`)
4. Follow DNS configuration instructions

### Environment Variables Reference

```env
# Required - Authentication
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-32-character-encryption-key

# Required - API Keys
OPENAI_API_KEY=sk-your-openai-key
WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856

# Optional - Notifications
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com

# Railway Auto-Generated
DATABASE_URL=postgresql://user:pass@host:port/database
RAILWAY_TCP_PROXY_DOMAIN=proxy.railway.app
RAILWAY_TCP_PROXY_PORT=your-port
```

### Monitoring & Scaling

1. **Monitor usage:**
   - Railway Dashboard → Usage
   - Track monthly credit consumption

2. **Set up alerts:**
   - Railway Dashboard → Settings → Billing
   - Set alerts at $5, $10, $20

3. **Scale when needed:**
   - Upgrade to paid plan for more resources
   - Add more containers for scaling

## 🚨 Troubleshooting

### Common Issues:

1. **Deployment fails:**
   ```bash
   # Check logs
   railway logs

   # Check status
   railway status

   # Rebuild
   railway up
   ```

2. **n8n not accessible:**
   - Check if port 5678 is exposed
   - Verify environment variables are set
   - Check Railway logs for errors

3. **Database connection issues:**
   - Verify DATABASE_URL is set
   - Check PostgreSQL is provisioned
   - Test connection manually

4. **API key issues:**
   - Verify all API keys are set correctly
   - Test API connectivity
   - Check rate limits and quotas

### Get Help:

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **n8n Community**: https://community.n8n.io

## 📊 Cost Monitoring

**Track your usage:**
```bash
# Check monthly usage
railway usage

# View billing dashboard
open https://railway.app/dashboard/billing
```

**Cost Breakdown:**
- **Free tier**: $5/month credit
- **n8n container**: ~$0.25/day (512MB RAM)
- **PostgreSQL**: Included in free tier
- **Estimated monthly cost**: $7.50 for full-time usage
- **With free credit**: First 20 days free each month

## 🎯 Next Steps After Deployment

1. **Import workflows** in n8n
2. **Test video generation** with a sample lesson
3. **Set up monitoring** and alerts
4. **Configure custom domain** (optional)
5. **Scale up** when ready for production

## 🚀 Ready to Deploy?

**Choose your path:**

1. **Start with Railway** (recommended) - Fastest deployment
2. **Follow the steps above** - Complete deployment guide
3. **Test your system** - Verify everything works
4. **Scale as needed** - Upgrade when ready

**Your ProfBrainRot system is ready for Railway deployment!** 🎉

Would you like me to walk you through the deployment step-by-step, or do you have any specific questions about the Railway setup?""""file_path":"C:\Users\CsányiIstván\My Drive\Private\Prof_BrainRot\RAILWAY_DEPLOYMENT_GUIDE.md