# Manual Setup Without Docker

If Docker is not available, you can run ProfBrainRot components manually. This guide walks you through setting up each component individually.

## 🏗️ Component Architecture

```
Manual Setup:
├── PostgreSQL (Database)
├── n8n (Workflow Engine)
├── Python Scripts (Video Processing)
└── Web Interface (Static HTML)
```

## 📋 Prerequisites

- **PostgreSQL**: Download from https://www.postgresql.org/download/
- **Node.js**: Download from https://nodejs.org/ (v16 or higher)
- **Python 3.8+**: Download from https://python.org/
- **Git**: Download from https://git-scm.com/

## 🚀 Step-by-Step Manual Setup

### 1. Install PostgreSQL

**Windows:**
1. Download installer from https://www.postgresql.org/download/windows/
2. Run installer, set password: `profbrainrot123`
3. Default port: 5432
4. Create database: `profbrainrot`

**Verify Installation:**
```cmd
psql -U postgres -d profbrainrot -c "SELECT version();"
```

### 2. Set Up Database

Run the schema script:
```cmd
psql -U postgres -d profbrainrot -f database/schema.sql
```

### 3. Install n8n Standalone

**Option A: npm Global Install**
```cmd
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

**Option B: Local Install**
```cmd
# Create n8n directory
mkdir n8n-standalone
cd n8n-standalone

# Install n8n locally
npm install n8n

# Create start script
echo const { start } = require('n8n'); start(); > start.js

# Start n8n
node start.js
```

**Access n8n:** http://localhost:5678

### 4. Configure n8n

1. **Set Environment Variables:**
   ```cmd
   set N8N_BASIC_AUTH_ACTIVE=true
   set N8N_BASIC_AUTH_USER=admin
   set N8N_BASIC_AUTH_PASSWORD=your-password
   set N8N_ENCRYPTION_KEY=your-32-character-encryption-key
   set DB_TYPE=postgresdb
   set DB_POSTGRESDB_HOST=localhost
   set DB_POSTGRESDB_PORT=5432
   set DB_POSTGRESDB_DATABASE=profbrainrot
   set DB_POSTGRESDB_USER=postgres
   set DB_POSTGRESDB_PASSWORD=profbrainrot123
   set OPENAI_API_KEY=your-openai-api-key
   set WAN25_API_KEY=sk-c3ba3cd1903c419bb24b7970ecd01856
   set PROCESSING_NOTIFICATION_EMAIL=your-email@example.com
   ```

2. **Import Workflows:**
   - Open http://localhost:5678
   - Click "Import" and select `n8n/workflows/lesson_processor.json`
   - Click "Import" and select `n8n/workflows/queue_processor_wan25.json`
   - Configure credentials for PostgreSQL, OpenAI, and Wan 2.5

### 5. Set Up Python Environment

**Create virtual environment:**
```cmd
cd Prof_BrainRot
python -m venv venv
venv\Scripts\activate  # On Windows
```

**Install dependencies:**
```bash
pip install requests psycopg2-binary
```

### 6. Create Python Queue Processor

Since n8n might not be running, create a Python script to handle queue processing:

```python
# queue_processor.py
import psycopg2
import requests
import time
import json
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="profbrainrot",
    user="postgres",
    password="profbrainrot123"
)

def process_queue():
    """Process video generation queue"""
    with conn.cursor() as cur:
        # Get next batch of videos to process
        cur.execute("""
            SELECT id, script_id, content, target_platform
            FROM video_queue
            WHERE status = 'queued' AND error_count < 3
            ORDER BY priority, created_at
            LIMIT 3
        """)

        videos = cur.fetchall()

        for video in videos:
            id, script_id, content, platform = video

            # Mark as processing
            cur.execute("""
                UPDATE video_queue
                SET status = 'processing', processing_started_at = NOW()
                WHERE id = %s
            """, (id,))

            # Generate video with Wan 2.5
            success = generate_wan25_video(script_id, content, platform)

            if success:
                cur.execute("""
                    UPDATE video_queue
                    SET status = 'completed', completed_at = NOW()
                    WHERE id = %s
                """, (id,))
            else:
                cur.execute("""
                    UPDATE video_queue
                    SET status = 'failed', error_count = error_count + 1
                    WHERE id = %s
                """, (id,))

            conn.commit()

def generate_wan25_video(script_id, content, platform):
    """Generate video using Wan 2.5 API"""
    api_key = "sk-c3ba3cd1903c419bb24b7970ecd01856"

    request_data = {
        "model": "wan2.5-t2v-preview",
        "input": {
            "prompt": content,
            "negative_prompt": "blurry, low quality, distracting elements, watermark, logo, text overlay"
        },
        "parameters": {
            "size": "1280*720",
            "duration": 10,
            "audio": True,
            "prompt_extend": True,
            "watermark": False
        }
    }

    try:
        # Submit task
        response = requests.post(
            "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable"
            },
            json=request_data
        )

        if response.status_code == 201:
            result = response.json()
            task_id = result.get("output", {}).get("task_id")

            # Poll for completion
            return poll_wan25_task(task_id, api_key, script_id)
        else:
            print(f"Task submission failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"Video generation error: {e}")
        return False

def poll_wan25_task(task_id, api_key, script_id):
    """Poll task until completion"""
    max_attempts = 20
    for attempt in range(max_attempts):
        try:
            response = requests.get(
                f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}",
                headers={"Authorization": f"Bearer {api_key}"}
            )

            if response.status_code == 200:
                result = response.json()
                status = result.get("output", {}).get("task_status")

                if status == "SUCCEEDED":
                    video_url = result.get("output", {}).get("video_url")
                    print(f"Video completed: {video_url}")

                    # Update database with video URL
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE video_queue
                            SET video_url = %s, video_duration = 10
                            WHERE script_id = %s
                        """, (video_url, script_id))
                        conn.commit()

                    return True
                elif status == "FAILED":
                    print(f"Task failed: {result.get('output', {}).get('message')}")
                    return False
                elif status in ["PENDING", "RUNNING"]:
                    print(f"Task {status}, waiting...")
                    time.sleep(30)
                    continue

        except Exception as e:
            print(f"Status check error: {e}")
            return False

    return False

if __name__ == "__main__":
    print("Starting manual queue processor...")
    while True:
        process_queue()
        time.sleep(60)  # Check every minute
```

### 7. Set Up Web Interface

The web interface is already created (`web/index.html`). You can:
- Open it directly in browser: `file:///path/to/web/index.html`
- Serve it with Python: `python -m http.server 8080` in the web directory
- Use any web server (Apache, Nginx, etc.)

### 8. Test the System

**Test API connection:**
```python
python tests/test_wan25_api_fixed.py
```

**Test video processing:**
```python
# Add a test record to queue
python -c "
import psycopg2
conn = psycopg2.connect(host='localhost', database='profbrainrot', user='postgres', password='profbrainrot123')
cur = conn.cursor()
cur.execute('INSERT INTO video_queue (lesson_id, lesson_title, script_id, script_type, content, hook_text, target_platform, priority, adhd_optimized, estimated_attention_span) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
('test_lesson_01', 'Test Lesson', 'test_script_01', 'short', 'A friendly teacher explaining basic math concepts with colorful animations.', 'Learn math in 30 seconds!', 'tiktok', 1, True, 30))
conn.commit()
conn.close()
print('Test record added to queue')
"
```

## 🔄 Alternative: Use Cloud Services

If local setup is too complex, consider:

1. **Railway.app** - Free tier available
2. **Render.com** - Free tier available
3. **Fly.io** - Free tier available
4. **Heroku** - Free tier available

## 📊 Monitoring Without Docker

**Check system status:**
```python
# Check queue status
python -c "
import psycopg2
conn = psycopg2.connect(host='localhost', database='profbrainrot', user='postgres', password='profbrainrot123')
cur = conn.cursor()
cur.execute('SELECT status, COUNT(*) FROM video_queue GROUP BY status')
for row in cur.fetchall():
    print(f'{row[0]}: {row[1]}')
conn.close()
"
```

## 🆘 Troubleshooting Manual Setup

**PostgreSQL won't start:**
- Check if port 5432 is free: `netstat -an | findstr 5432`
- Verify PostgreSQL service is running
- Check Windows Event Viewer for errors

**n8n won't start:**
- Check if port 5678 is free: `netstat -an | findstr 5678`
- Verify Node.js is installed: `node --version`
- Check n8n logs in the terminal

**API calls fail:**
- Verify API keys in environment variables
- Check internet connection
- Test API directly with curl/Python

**Videos won't generate:**
- Check Wan 2.5 API quota and billing
- Verify PostgreSQL connection
- Check error logs in database

## 🎯 Next Steps

1. **Choose your setup method** (Docker or Manual)
2. **Install required software** (PostgreSQL, Node.js, Python)
3. **Configure components** (database, n8n, API keys)
4. **Test the system** (API connection, video generation)
5. **Start processing** (upload lesson plans, monitor queue)

**The system is ready - you just need to choose your preferred installation method!** 🚀

Would you like me to help you with Docker installation, or would you prefer to set up the manual configuration?"}