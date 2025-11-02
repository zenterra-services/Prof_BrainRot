# Cloud Deployment Guide for ProfBrainRot

Deploy your ProfBrainRot system to the cloud for scalability, reliability, and easy management. This guide covers the best cloud platforms for 2025 with free tiers and cost-effective scaling.

## 🏆 **Recommended Cloud Platforms (2025)**

### **1. Oracle Cloud Infrastructure (OCI) - BEST FREE TIER**
- **Free Forever**: 4-core ARM VM + 20GB managed PostgreSQL
- **Perfect for**: 24/7 production without costs
- **Setup time**: ~30 minutes

### **2. Render - EASIEST SETUP**
- **Free tier**: 512MB RAM, sleeps after 15min idle
- **Perfect for**: Development and low-traffic apps
- **Setup time**: ~15 minutes

### **3. Railway - DEVELOPER FRIENDLY**
- **Free tier**: $5/month credit (~20 days full-time)
- **Perfect for**: Quick prototypes and experiments
- **Setup time**: ~10 minutes

### **4. Fly.io - PERFORMANCE FOCUSED**
- **Cost**: ~$4.30/month for micro setup
- **Perfect for**: High-performance, global deployment
- **Setup time**: ~20 minutes

---

## 🚀 **Oracle Cloud Infrastructure (RECOMMENDED)**

### **Why Oracle Cloud?**
- ✅ **Truly free forever** (no credit card expiry)
- ✅ **4-core ARM VM + 24GB RAM** (massive overkill)
- ✅ **20GB managed PostgreSQL** (always free)
- ✅ **Handles 50+ concurrent workflows easily**

### **Step 1: Create Oracle Cloud Account**
1. Go to https://cloud.oracle.com
2. Click "Sign Up" → "Oracle Cloud Free Tier"
3. Complete registration (credit card required for verification only)
4. Verify email and log in

### **Step 2: Create Compartment**
1. Console → Identity → Compartments
2. Click "Create Compartment"
3. Name: `profbrainrot-prod`
4. Description: "Production environment for ProfBrainRot"
5. Click "Create"

### **Step 3: Create Virtual Cloud Network (VCN)**
1. Console → Networking → Virtual Cloud Networks
2. Click "Create VCN"
3. Name: `profbrainrot-vcn`
4. IPv4 CIDR Block: `10.0.0.0/16`
5. Click "Create"

### **Step 4: Create PostgreSQL Database**
1. Console → Databases → Autonomous Database
2. Click "Create Autonomous Database"
3. Configuration:
   - **Compartment**: `profbrainrot-prod`
   - **Display Name**: `profbrainrot-db`
   - **Database Name**: `PROFBRAINROT`
   - **Workload Type**: `Transaction Processing`
   - **Deployment Type**: `Shared Infrastructure`
   - **Always Free**: ✅ Checked
4. Administrator Credentials:
   - **Username**: `ADMIN`
   - **Password**: `ProfBrainRot2025!`
5. Click "Create Autonomous Database"
6. Wait for status: **AVAILABLE** (5-10 minutes)

### **Step 5: Get Database Connection Info**
1. Click on your database → **DB Connection**
2. Note down:
   - **Username**: `ADMIN`
   - **Password**: `ProfBrainRot2025!`
   - **Connection String**: Copy the **TLS** connection string

### **Step 6: Create Compute Instance**
1. Console → Compute → Instances
2. Click "Create Instance"
3. Configuration:
   - **Name**: `profbrainrot-server`
   - **Compartment**: `profbrainrot-prod`
   - **Image**: **Oracle Linux 8** (ARM)
   - **Shape**: **VM.Standard.A1.Flex** (4 OCPU, 24 GB RAM)
   - **Always Free Eligible**: ✅ Checked
4. Networking:
   - **VCN**: `profbrainrot-vcn`
   - **Subnet**: Choose public subnet
   - **Assign Public IP**: ✅ Checked
5. Add SSH Keys:
   - Generate new: `ssh-keygen -t rsa -b 4096 -f ~/.ssh/oci_key`
   - Or paste existing public key
6. Click "Create"
7. Wait for status: **RUNNING** (2-3 minutes)

### **Step 7: Connect to Instance**
1. Note the **Public IP Address**
2. SSH into instance:
   ```bash
   ssh -i ~/.ssh/oci_key opc@YOUR_PUBLIC_IP
   ```

### **Step 8: Install Docker on Oracle Linux**
```bash
# Update system
sudo dnf update -y

# Install Docker
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io -y

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker opc
newgrp docker
```

### **Step 9: Deploy ProfBrainRot**
```bash
# Clone repository
git clone https://github.com/zenterra-services/Prof_BrainRot.git
cd Prof_BrainRot

# Create environment file
cat > .env << EOF
# Database (Oracle Autonomous Database)
POSTGRES_HOST=your-db-host.oraclecloud.com
POSTGRES_PORT=1521
POSTGRES_DATABASE=PROFBRAINROT
POSTGRES_USER=ADMIN
POSTGRES_PASSWORD=ProfBrainRot2025!

# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-32-character-encryption-key

# API Keys
OPENAI_API_KEY=your-openai-api-key
WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com

# Oracle Cloud specific
ORACLE_CLOUD_REGION=us-ashburn-1
ORACLE_CLOUD_TENANCY=your-tenancy-ocid
ORACLE_CLOUD_USER=your-user-ocid
EOF

# Create Docker Compose for Oracle Cloud
cat > docker-compose.yml << EOF
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your-secure-password
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_ENCRYPTION_KEY=your-32-character-encryption-key
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=your-db-host.oraclecloud.com
      - DB_POSTGRESDB_PORT=1521
      - DB_POSTGRESDB_DATABASE=PROFBRAINROT
      - DB_POSTGRESDB_USER=ADMIN
      - DB_POSTGRESDB_PASSWORD=ProfBrainRot2025!
      - OPENAI_API_KEY=your-openai-api-key
      - WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856
      - PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n/workflows:/workflows
    restart: unless-stopped

volumes:
  n8n_data:
EOF

# Start services
docker-compose up -d
```

### **Step 10: Configure Security Rules**
1. Console → Networking → Security Lists
2. Select your VCN's security list
3. Add Ingress Rules:
   ```
   Source: 0.0.0.0/0
   Protocol: TCP
   Port: 5678
   Description: n8n web interface
   ```

### **Step 11: Access Your System**
1. **n8n Dashboard**: http://YOUR_PUBLIC_IP:5678
2. **Import workflows** from `/n8n/workflows/`
3. **Configure credentials** for PostgreSQL, OpenAI, Wan 2.5

### **Step 12: Monitor Costs**
```bash
# Check usage in Oracle Cloud Console
# Billing → Cost Analysis
# Set filter to your compartment
```

---

## 🚂 **Railway Deployment (Easiest)**

### **Why Railway?**
- ✅ **Git-push deployment** (easiest workflow)
- ✅ **$5/month credit** (covers ~20 days full-time)
- ✅ **Managed PostgreSQL** included
- ✅ **Automatic SSL** and custom domains

### **Step 1: Create Railway Account**
1. Go to https://railway.app
2. Sign up with GitHub
3. Verify email

### **Step 2: Connect GitHub Repository**
1. Click "New Project"
2. Choose "Deploy from GitHub"
3. Select your ProfBrainRot repository
4. Authorize Railway to access your repo

### **Step 3: Create Railway Configuration**
Create `railway.json` in your repository:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "railway.Dockerfile"
  },
  "deploy": {
    "startCommand": "docker-compose up",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### **Step 4: Create Railway Dockerfile**
Create `railway.Dockerfile`:
```dockerfile
FROM n8nio/n8n:latest

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy workflows
COPY n8n/workflows /workflows

# Set environment variables (Railway will inject these)
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV DB_TYPE=postgresdb

# Start n8n
CMD ["n8n", "start"]
```

### **Step 5: Configure Environment Variables**
In Railway dashboard:
1. Go to your project → **Variables**
2. Add these variables:
   ```
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=your-secure-password
   N8N_ENCRYPTION_KEY=your-32-character-encryption-key
   DB_POSTGRESDB_HOST=${{RAILWAY_TCP_PROXY_DOMAIN}}
   DB_POSTGRESDB_PORT=${{RAILWAY_TCP_PROXY_PORT}}
   DB_POSTGRESDB_DATABASE=railway
   DB_POSTGRESDB_USER=postgres
   DB_POSTGRESDB_PASSWORD=${{DATABASE_URL}}
   OPENAI_API_KEY=your-openai-api-key
   WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856
   PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
   ```

### **Step 6: Deploy**
1. Push code to GitHub
2. Railway automatically builds and deploys
3. Monitor deployment logs in Railway dashboard

### **Step 7: Access Your System**
1. Railway provides a URL like `https://profbrainrot-production.up.railway.app`
2. Access n8n at: `https://profbrainrot-production.up.railway.app:5678`
3. Import workflows and configure credentials

### **Step 8: Monitor Usage**
1. Railway Dashboard → **Usage**
2. Track monthly credit consumption
3. Set up billing alerts when approaching limits

---

## 🚀 **Quick Start Comparison**

| Platform | Setup Time | Free Tier | Best For | Monthly Cost (Paid) |
|----------|------------|-----------|----------|-------------------|
| **Oracle Cloud** | 30 min | Forever | Production, 24/7 | $0 |
| **Railway** | 10 min | $5 credit | Quick prototypes | $5+ |
| **Render** | 15 min | 512MB + sleep | Development | $14+ |
| **Fly.io** | 20 min | None | Performance | $4.30+ |

---

## 🎯 **My Recommendation**

**For your ProfBrainRot system, I recommend:**

1. **Start with Railway** (10 minutes) - Get it running quickly
2. **Move to Oracle Cloud** (when ready) - For 24/7 production
3. **Keep Railway as backup** - For development/testing

**Why this approach?**
- Railway gets you running in 10 minutes
- Oracle Cloud gives you truly free, unlimited production
- You can migrate between them easily
- Both support Docker containers perfectly

---

## 🚀 **Let's Get Started!**

**Choose your preferred platform:**

1. **Railway** (fastest setup) → Start here
2. **Oracle Cloud** (best long-term) → Move here later
3. **Render** (developer-friendly) → Alternative option

**Which platform would you like to deploy to first?** I can walk you through the complete setup step-by-step! 🎯

Once you choose, I'll provide the exact deployment commands and configuration files for your ProfBrainRot system."}