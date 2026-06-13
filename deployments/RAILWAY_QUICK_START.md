# Railway Quick Start Guide

Deploy your ProfBrainRot system to Railway in under 10 minutes! Railway offers the easiest Git-push deployment with managed PostgreSQL and automatic scaling.

## 🚀 **Why Railway?**
- ✅ **Git-push deployment** (easiest workflow)
- ✅ **$5/month credit** (covers ~20 days full-time)
- ✅ **Managed PostgreSQL** included
- ✅ **Automatic SSL** and custom domains
- ✅ **10-minute setup** from zero to production

## 📋 **Prerequisites**
- GitHub account
- Railway account (free)
- Your API keys:
  - OpenAI API key
  - Wan 2.5 API key: `${WAN25_API_KEY}`

## 🚂 **Step-by-Step Railway Deployment**

### **Step 1: Create Railway Account**
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Verify your email

### **Step 2: Prepare Your Repository**
Make sure your repository has the Railway deployment files:

```bash
# Your repository structure should be:
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

### **Step 3: Install Railway CLI (Optional but Recommended)**
```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login to Railway
railway login
```

### **Step 4: Create New Railway Project**
```bash
# Navigate to your project directory
cd Prof_BrainRot

# Initialize Railway project
railway init --name profbrainrot --template docker

# Or use the web interface:
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Choose "Deploy from GitHub"
# 4. Select your ProfBrainRot repository
```

### **Step 5: Configure Environment Variables**

**Option A: Using Railway CLI**
```bash
# Set environment variables
railway variables set \
    N8N_BASIC_AUTH_USER=admin \
    N8N_BASIC_AUTH_PASSWORD=your-secure-password \
    N8N_ENCRYPTION_KEY=your-32-character-encryption-key \
    OPENAI_API_KEY=your-openai-api-key \
    WAN25_API_KEY=${WAN25_API_KEY} \
    PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
```

**Option B: Using Web Interface**
1. Go to your Railway project dashboard
2. Click on your project
3. Go to **Variables** tab
4. Add these variables one by one:

```env
# Authentication
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-32-character-encryption-key

# API Keys
OPENAI_API_KEY=your-openai-api-key
WAN25_API_KEY=${WAN25_API_KEY}

# Notifications
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
```

### **Step 6: Deploy Your Application**

**Using Git (Recommended):**
```bash
# Add Railway remote (if using CLI)
railway login

# Push to deploy
git add .
git commit -m "Deploy to Railway with Wan 2.5 integration"
git push origin main
```

**Using Railway Dashboard:**
1. Push your code to GitHub
2. Railway automatically detects changes and builds
3. Monitor build progress in Railway dashboard

### **Step 7: Monitor Deployment**
```bash
# Check deployment status
railway status

# View logs
railway logs

# Or use web interface:
# Railway Dashboard → Your Project → Deployments
```

### **Step 8: Access Your System**

Railway will provide you with a URL like:
`https://profbrainrot-production.up.railway.app`

1. **Access n8n**: `https://profbrainrot-production.up.railway.app`
2. **Login**: Use your configured username/password
3. **Import workflows**: Upload `lesson_processor.json` and `queue_processor_wan25.json`
4. **Configure credentials**: Set up PostgreSQL, OpenAI, and Wan 2.5 credentials

## 🔧 **Railway-Specific Configuration**

### **Environment Variables Reference**
```env
# Railway automatically provides these:
DATABASE_URL=postgresql://user:pass@host:port/database
RAILWAY_TCP_PROXY_DOMAIN=proxy.railway.app
RAILWAY_TCP_PROXY_PORT=your-port

# You need to set these:
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-32-character-encryption-key
OPENAI_API_KEY=your-openai-api-key
WAN25_API_KEY=${WAN25_API_KEY}
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
```

### **Railway PostgreSQL Connection**
Railway provides managed PostgreSQL automatically. The connection details are injected via `DATABASE_URL` environment variable.

### **Custom Domain (Optional)**
1. Railway Dashboard → Settings → Domains
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `profbrainrot.yourdomain.com`)
4. Follow DNS configuration instructions

## 📊 **Cost Monitoring**

### **Track Usage**
```bash
# Check monthly usage
railway usage

# View billing dashboard
open https://railway.app/dashboard/billing
```

### **Set Up Alerts**
1. Railway Dashboard → Settings → Billing
2. Set billing alerts at $5, $10, $20
3. Configure email notifications

### **Cost Breakdown**
- **Free tier**: $5/month credit
- **n8n container**: ~$0.25/day (512MB RAM)
- **PostgreSQL**: Included in free tier
- **Estimated monthly cost**: $7.50 for full-time usage
- **With free credit**: First 20 days free each month

## 🚨 **Troubleshooting**

### **Deployment Fails**
```bash
# Check logs
railway logs

# Rebuild
railway up

# Check environment variables
railway variables
```

### **n8n Not Accessible**
1. Check if container is running: `railway status`
2. Verify port 5678 is exposed
3. Check environment variables are set
4. Review n8n logs for errors

### **Database Connection Issues**
1. Verify `DATABASE_URL` is set
2. Check PostgreSQL is provisioned
3. Test connection manually

### **API Key Issues**
1. Verify all API keys are set correctly
2. Test Wan 2.5 API separately
3. Check rate limits and quotas

## 🎯 **Next Steps After Deployment**

1. **Import workflows** in n8n
2. **Test video generation** with a sample lesson
3. **Set up monitoring** and alerts
4. **Configure custom domain** (optional)
5. **Scale up** when ready for production

## 📞 **Support**

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **n8n Community**: https://community.n8n.io
- **Oracle Cloud Support**: Through Railway dashboard

---

**🚀 Ready to deploy? Choose your platform and let's get your ProfBrainRot system running in the cloud!**

Would you like me to walk you through the Railway deployment step-by-step, or would you prefer to start with Oracle Cloud for the free forever option?""""file_path":"C:\Users\CsányiIstván\My Drive\Private\Prof_BrainRot\deployments\RAILWAY_QUICK_START.md"}