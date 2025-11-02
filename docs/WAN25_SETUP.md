# Wan 2.5 Integration Setup Guide

This guide walks you through setting up Wan 2.5 as your primary video generator, which will save you approximately **$16.50/month** compared to Zebracat while providing better quality videos with native audio.

## 💰 Cost Comparison

| Service | Monthly Cost | Videos | Cost per Video | Quality |
|---------|-------------|---------|----------------|---------|
| Zebracat | $19.50 | 60 | $0.33 | 720p |
| **Wan 2.5** | **~$3.00** | **60** | **$0.05** | **1080p + Audio** |
| **Savings** | **$16.50** | - | **85% less** | **Better** |

## 🚀 Quick Setup Steps

### 1. Get Wan 2.5 API Key

1. **Sign up for Alibaba Cloud**: https://www.alibabacloud.com
2. **Navigate to Model Studio**: Console → Products → AI → Model Studio
3. **Create API Key**:
   - Go to "API Keys" section
   - Click "Create API Key"
   - Copy your DashScope API key
4. **Enable Billing**: Add payment method (pay-as-you-go)

### 2. Configure Environment

Update your `.env` file:

```bash
# Wan 2.5 API Configuration
WAN25_API_KEY=your-dashscope-api-key-here
WAN25_REGION=intl  # Use 'intl' for Singapore or 'cn' for Beijing

# Optional: Keep Zebracat as backup (commented out by default)
# ZEBRACAT_API_KEY=your-zebracat-api-key-here
```

### 3. Import Updated Workflow

1. **Open n8n**: http://localhost:5678
2. **Import Workflow**:
   - Click "Import"
   - Select `queue_processor_wan25.json`
   - Or copy the JSON content and paste

### 4. Configure API Credentials

1. **Add Wan 2.5 Credential**:
   - Go to Credentials → Add Credential
   - Type: "Header Auth"
   - Name: "Wan 2.5 API Key"
   - Headers:
     ```
     Authorization: Bearer YOUR_API_KEY
     ```

2. **Update Workflow References**:
   - Open the imported workflow
   - Update all "Wan 2.5 API Key" credential references
   - Save the workflow

### 5. Test the Integration

1. **Upload a Lesson**: Use the web interface
2. **Monitor Processing**: Check n8n execution logs
3. **Verify Output**: Videos should be 10 seconds, 720p, with audio

## 📋 API Configuration Details

### Request Parameters (Educational Optimized)

```json
{
  "model": "wan2.5-t2v-preview",
  "input": {
    "prompt": "{{ educational_script_content }}",
    "negative_prompt": "blurry, low quality, distracting elements, watermark, logo, text overlay, shaky camera, poor lighting, inappropriate content"
  },
  "parameters": {
    "size": "1280*720",        // 720p for optimal quality/cost
    "duration": 10,            // 10 seconds (perfect for ADHD attention span)
    "audio": true,             // Include native audio generation
    "prompt_extend": true,     // AI will enhance your prompt
    "watermark": false,        // Clean educational videos
    "seed": {{ random_seed }}  // For reproducible results
  }
}
```

### Regional Endpoints

| Region | Endpoint | Use Case |
|--------|----------|----------|
| **Singapore (intl)** | `https://dashscope-intl.aliyuncs.com` | **Recommended for international users** |
| Beijing (cn) | `https://dashscope.aliyuncs.com` | For China-based users |

### Rate Limits

- **Submission Rate**: 5 requests per second
- **Concurrent Tasks**: 5 maximum
- **Processing Time**: 30-120 seconds per video

## 🎥 Video Specifications

### Output Format
- **Format**: MP4 (H.264)
- **Resolution**: 1280x720 (720p)
- **Duration**: 10 seconds
- **Frame Rate**: 30 FPS
- **Audio**: AAC stereo, generated from text
- **File Size**: ~2-5 MB per video
- **URL Expiry**: 24 hours (download immediately)

### ADHD Optimization Features
- **Duration**: 10 seconds (optimal for attention span)
- **Audio**: Native generation for better engagement
- **Quality**: 720p clear visuals
- **Pacing**: Consistent frame rate, smooth transitions

## 🔧 Troubleshooting

### Common Issues

#### 1. "Invalid API Key" Error
```
Solution:
- Verify API key is correct
- Check if billing is enabled
- Ensure region matches your setting
```

#### 2. "Task Failed" Error
```
Solution:
- Check negative prompt for invalid characters
- Reduce prompt length if >2000 chars
- Try different seed value
```

#### 3. "Rate Limit Exceeded"
```
Solution:
- Reduce batch size to 1-2 videos
- Increase wait time between requests
- Check concurrent task limit
```

#### 4. "Content Moderated"
```
Solution:
- Ensure educational content only
- Remove any sensitive topics
- Use more specific negative prompts
```

### Debug Steps

1. **Check n8n Logs**:
   ```bash
   docker-compose logs n8n | grep -i wan
   ```

2. **Verify API Key**:
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" \
        -H "X-DashScope-Async: enable" \
        https://dashscope-intl.aliyuncs.com/api/v1/users/me
   ```

3. **Test Direct API**:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json" \
     -H "X-DashScope-Async: enable" \
     -d '{
       "model": "wan2.5-t2v-preview",
       "input": {
         "prompt": "A simple educational animation about math",
         "negative_prompt": "blurry, low quality"
       },
       "parameters": {
         "size": "1280*720",
         "duration": 5,
         "audio": true
       }
     }' \
     https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
   ```

## 📊 Cost Monitoring

### Track Usage
```sql
-- Monthly usage summary
SELECT
    COUNT(*) as videos_created,
    SUM(CASE WHEN api_provider = 'wan2.5' THEN 1 ELSE 0 END) as wan25_videos,
    SUM(CASE WHEN status_code = 200 THEN 10 ELSE 0 END) as estimated_seconds,
    SUM(CASE WHEN status_code = 200 THEN 10 * 0.10 ELSE 0 END) as estimated_cost_usd
FROM api_usage_log
WHERE created_at >= date_trunc('month', CURRENT_DATE);
```

### Budget Alerts
Set up email notifications when monthly costs exceed:
- $5 (50 videos)
- $10 (100 videos)
- $20 (200 videos)

## 🔄 Migration from Zebracat

### Steps to Switch
1. **Update Environment**: Add Wan 2.5 keys, comment out Zebracat
2. **Import New Workflow**: Use `queue_processor_wan25.json`
3. **Update Credentials**: Change API key references
4. **Test Processing**: Verify with small batch
5. **Monitor Costs**: Track usage for first month

### Rollback Plan
Keep Zebracat credentials as backup:
```bash
# Emergency fallback
ZEBRACAT_API_KEY=your-backup-key
# Update workflow to use Zebracat if Wan 2.5 fails
```

## 🚀 Advanced Configuration

### Custom Parameters
Modify these in the n8n workflow for different use cases:

```javascript
// For younger students (shorter, simpler)
"duration": 5,
"size": "832*480",

// For older students (longer, detailed)
"duration": 10,
"size": "1920*1080",

// Without audio (if needed)
"audio": false,

// With custom seed for consistency
"seed": 12345,
```

### Quality vs Cost Optimization
- **480p**: $0.05/second (budget option)
- **720p**: $0.10/second (recommended balance)
- **1080p**: $0.15/second (premium quality)

## 📞 Support

### Alibaba Cloud Support
- **Documentation**: https://www.alibabacloud.com/help/en/model-studio/
- **Support Tickets**: Console → Support → Tickets
- **Community**: Alibaba Cloud forums

### Integration Help
- Check n8n community forums
- Review error logs in PostgreSQL
- Monitor email notifications

---

**Next Steps**: After setup, test with a few videos and monitor the costs. You should see significant savings while getting better quality videos with native audio!