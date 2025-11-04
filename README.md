# ProfBrainRot - ADHD-Friendly Educational Video Generator

Transform traditional lesson plans into engaging short-form videos optimized for ADHD learners. Built with n8n automation and budget-friendly video generation APIs.

## 🎯 Project Overview

ProfBrainRot converts educational content into TikTok-style short videos (30-60 seconds) and longer YouTube content (8-10 minutes) using research-backed ADHD optimization techniques. The system maintains a queue-based pipeline for processing multiple videos in small batches (2-3 videos) perfect for personal use.

## 🧠 Key Features

- **ADHD-Optimized Content**: Videos designed with natural pause points and controllable pacing
- **Multi-Platform Output**: TikTok, YouTube Shorts, Instagram Reels, and long-form YouTube
- **Queue-Based Processing**: PostgreSQL queue system for managing video generation
- **Budget-Friendly**: Uses Wan 2.5 API (85% cost savings vs competitors)
- **n8n Automation**: Complete workflow automation with error handling and retry logic
- **Kréta LMS Integration**: Ready for Hungarian education system integration

## 🏗️ Architecture

```
Lesson Plan → AI Script Generation → Queue Storage → Video Generation → Platform Optimization → Publishing
```

### Components

1. **Web Interface** (`/web/index.html`) - Simple upload form and status monitoring
2. **n8n Workflows** (`/n8n/workflows/`) - Automation pipelines
3. **PostgreSQL Database** - Queue management and data storage
4. **Video Generation APIs** - Wan 2.5 (primary, 85% cost savings!), Zebracat (backup)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Wan 2.5 API key (recommended - 85% cost savings!)
- SMTP credentials for email notifications (optional)

### 1. Clone and Setup

```bash
git clone https://github.com/zenterra-services/Prof_BrainRot.git
cd Prof_BrainRot
```

### 2. Configure Environment

```bash
cp n8n/.env.example n8n/.env
# Edit n8n/.env with your API keys and settings
```

### 3. Start Services

```bash
cd n8n
docker-compose up -d
```

### 4. Access Services

- **n8n Workflow Editor**: http://localhost:5678
- **Web Interface**: Open `/web/index.html` in your browser
- **PostgreSQL**: localhost:5432 (profbrainrot/profbrainrot123)

### 5. Import Workflows

1. Open n8n at http://localhost:5678
2. Import workflows from `/n8n/workflows/` folder:
   - `lesson_processor.json` - Processes lesson plans into scripts
   - `queue_processor_wan25.json` - Handles video generation with Wan 2.5
3. Configure credentials in n8n for:
   - PostgreSQL database
   - OpenAI API
   - Wan 2.5 API (see [WAN25_SETUP.md](docs/WAN25_SETUP.md))
   - SMTP (for notifications)

## 📊 Database Schema

### Core Tables

- **lessons** - Stores original lesson plans
- **video_queue** - Queue for video generation requests
- **processing_batches** - Manages 2-3 video batches
- **api_usage_log** - Tracks API usage and costs
- **error_log** - Error tracking and debugging

### Queue Status Flow

```
queued → processing → completed/failed/cancelled
```

## 🎥 Video Generation Pipeline

### Short Form (30-60 seconds)
- **Hook**: 0-3 seconds - Attention-grabbing opening
- **Content**: 3-25 seconds - Educational material
- **Call-to-action**: 25-28 seconds - Next steps

### Long Form (8-10 minutes)
- **Introduction**: 0-60 seconds
- **Main content**: 4-6 chapters with natural breaks
- **Summary**: Final 60 seconds

### ADHD Optimization Features
- Natural pause points every 10-15 seconds
- Controllable pacing (speed adjustment)
- Minimal executive function required to access
- Structured series (not endless scroll)

## 🔧 Configuration

### Environment Variables

```bash
# Required API Keys
OPENAI_API_KEY=sk-your-openai-key
WAN25_API_KEY=your-dashscope-api-key-here
WAN25_REGION=intl  # Use 'intl' for Singapore or 'cn' for Beijing

# Database
POSTGRES_PASSWORD=your-secure-password

# n8n Security
N8N_USER=admin
N8N_PASSWORD=your-n8n-password
N8N_ENCRYPTION_KEY=your-32-char-encryption-key

# Email Notifications
PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional: Backup APIs
# ZEBRACAT_API_KEY=your-zebracat-api-key-here
```

### Batch Processing Settings

- **Batch Size**: 2-3 videos (configurable in n8n workflow)
- **Processing Interval**: Every 10 minutes
- **Retry Attempts**: Maximum 3 per video
- **Rate Limiting**: Respects API quotas

## 📈 Monitoring

### Queue Status
- Real-time queue statistics
- Processing success/failure rates
- API usage tracking
- Error logging and alerts

### Email Notifications
- Daily queue summaries
- Error alerts for failed videos
- Processing completion notifications

## 🔗 API Integration

### Wan 2.5 API (Primary - Recommended)
- Cost: ~$3/month for 60 videos (85% savings!)
- Features: 1080p with native audio generation
- Rate limit: 5 req/s, 5 concurrent tasks
- Duration: 5-10 seconds (perfect for shorts)
- Setup: See [WAN25_SETUP.md](docs/WAN25_SETUP.md)

### Zebracat API (Backup)
- Cost: ~$19.50/month for 60 HD videos
- Features: Text-to-video, educational templates
- Rate limit: 60 videos/hour
- Use case: Fallback option if needed

### Kréta LMS Integration (Future)
- Hungarian education system API
- OAuth2 authentication
- Lesson plan extraction
- Curriculum alignment

## 🛠️ Development

### Adding New Video APIs

1. Create new HTTP request node in n8n
2. Add API credentials to environment
3. Update queue processor workflow
4. Test with small batch

### Customizing Scripts

Modify the OpenAI prompt in `lesson_processor.json`:
- Adjust video length
- Change tone/style
- Add platform-specific requirements
- Modify ADHD optimization parameters

### Scaling Up

For public release (>100 videos/month):
1. Add Redis for better queue management
2. Increase worker containers
3. Upgrade to enterprise video APIs
4. Add load balancing

## 📚 Research-Based Design

This system implements findings from educational research:

- **9% exam score improvement** with properly designed short-form content
- **24.7% engagement increase** vs traditional methods
- **ADHD optimization**: Structured content avoids endless scroll pitfalls
- **30/60/10 rule**: 30% hook, 60% content, 10% call-to-action

## 🐛 Troubleshooting

### Common Issues

1. **n8n not starting**: Check PostgreSQL connection
2. **Video generation failing**: Verify API keys and quotas
3. **Queue stuck**: Check error logs in PostgreSQL
4. **Webhook not responding**: Ensure n8n is running and accessible

### Debug Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs n8n
docker-compose logs postgres

# Check queue status
docker-compose exec postgres psql -U profbrainrot -d profbrainrot -c "SELECT * FROM queue_status_summary;"
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test with personal use cases
4. Submit pull request with description

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Research on ADHD and short-form educational content
- n8n community for workflow automation
- Hungarian education system (Kréta LMS) developers
- OpenAI for script generation capabilities

---

**Note**: This is designed for personal use initially. Scale up gradually and monitor costs carefully when releasing to public.