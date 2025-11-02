-- Prof_BrainRot Video Generation Queue Schema
-- Designed for personal use with 2-3 video batches

-- Main queue table for storing generated scripts waiting for video creation
CREATE TABLE video_queue (
    id SERIAL PRIMARY KEY,
    lesson_id VARCHAR(100) NOT NULL,
    lesson_title VARCHAR(255) NOT NULL,
    script_id VARCHAR(100) UNIQUE NOT NULL,
    script_type VARCHAR(20) CHECK (script_type IN ('short', 'long')) NOT NULL,
    content TEXT NOT NULL,
    hook_text VARCHAR(255),
    target_platform VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')),
    priority INTEGER DEFAULT 1 CHECK (priority BETWEEN 1 AND 5),
    batch_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started_at TIMESTAMP,
    completed_at TIMESTAMP,
    video_url TEXT,
    video_duration INTEGER, -- in seconds
    error_count INTEGER DEFAULT 0 CHECK (error_count BETWEEN 0 AND 3),
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    -- ADHD optimization fields
    adhd_optimized BOOLEAN DEFAULT true,
    estimated_attention_span INTEGER, -- in seconds
    natural_pause_points INTEGER[] -- array of timestamps
);

-- Index for efficient queue processing
CREATE INDEX idx_video_queue_status_priority ON video_queue(status, priority, created_at);
CREATE INDEX idx_video_queue_batch_id ON video_queue(batch_id);
CREATE INDEX idx_video_queue_lesson_id ON video_queue(lesson_id);
CREATE INDEX idx_video_queue_script_type ON video_queue(script_type);

-- Lessons table to track original lesson plans
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    lesson_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    grade_level VARCHAR(20) NOT NULL,
    original_content TEXT NOT NULL,
    content_format VARCHAR(50) DEFAULT 'text', -- text, pdf, docx, etc.
    source_type VARCHAR(50) DEFAULT 'manual', -- manual, kreta, textbook
    source_reference TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    -- Processing status
    processing_status VARCHAR(50) DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
    total_scripts_generated INTEGER DEFAULT 0,
    total_videos_created INTEGER DEFAULT 0
);

-- Video generation API usage tracking
CREATE TABLE api_usage_log (
    id SERIAL PRIMARY KEY,
    script_id VARCHAR(100) REFERENCES video_queue(script_id),
    api_provider VARCHAR(50) NOT NULL, -- zebracat, invideo, etc.
    api_endpoint VARCHAR(255),
    request_type VARCHAR(50),
    status_code INTEGER,
    response_time INTEGER, -- in milliseconds
    cost_cents INTEGER, -- cost in cents for tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'
);

-- Processing batches for managing 2-3 video groups
CREATE TABLE processing_batches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(100) UNIQUE NOT NULL,
    lesson_id VARCHAR(100) REFERENCES lessons(lesson_id),
    batch_type VARCHAR(50) DEFAULT 'mixed', -- shorts_only, long_only, mixed
    total_items INTEGER DEFAULT 0,
    processed_items INTEGER DEFAULT 0,
    failed_items INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'created' CHECK (status IN ('created', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Error log for debugging
CREATE TABLE error_log (
    id SERIAL PRIMARY KEY,
    script_id VARCHAR(100) REFERENCES video_queue(script_id),
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT NOT NULL,
    error_context JSONB DEFAULT '{}',
    retry_attempt INTEGER DEFAULT 0,
    resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform posting schedule
CREATE TABLE posting_schedule (
    id SERIAL PRIMARY KEY,
    script_id VARCHAR(100) REFERENCES video_queue(script_id),
    platform VARCHAR(50) NOT NULL,
    scheduled_for TIMESTAMP NOT NULL,
    posted_at TIMESTAMP,
    post_url TEXT,
    post_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'posted', 'failed', 'cancelled')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Views for common queries
CREATE VIEW queue_status_summary AS
SELECT
    status,
    script_type,
    target_platform,
    COUNT(*) as count,
    MIN(created_at) as oldest_item,
    MAX(created_at) as newest_item
FROM video_queue
GROUP BY status, script_type, target_platform;

CREATE VIEW lesson_progress AS
SELECT
    l.lesson_id,
    l.title,
    l.subject,
    l.processing_status,
    l.total_scripts_generated,
    l.total_videos_created,
    COUNT(vq.id) as videos_in_queue,
    COUNT(CASE WHEN vq.status = 'completed' THEN 1 END) as videos_completed,
    COUNT(CASE WHEN vq.status = 'failed' THEN 1 END) as videos_failed
FROM lessons l
LEFT JOIN video_queue vq ON l.lesson_id = vq.lesson_id
GROUP BY l.lesson_id, l.title, l.subject, l.processing_status, l.total_scripts_generated, l.total_videos_created;

-- Helper functions
CREATE OR REPLACE FUNCTION get_next_batch(batch_size INTEGER DEFAULT 3)
RETURNS TABLE (
    id INTEGER,
    script_id VARCHAR,
    content TEXT,
    script_type VARCHAR,
    target_platform VARCHAR,
    priority INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT vq.id, vq.script_id, vq.content, vq.script_type, vq.target_platform, vq.priority
    FROM video_queue vq
    WHERE vq.status = 'queued'
      AND vq.error_count < 3
    ORDER BY vq.priority ASC, vq.created_at ASC
    LIMIT batch_size;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mark_batch_processing(batch_script_ids TEXT[])
RETURNS VOID AS $$
BEGIN
    UPDATE video_queue
    SET status = 'processing',
        processing_started_at = CURRENT_TIMESTAMP,
        batch_id = 'batch_' || to_char(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS')
    WHERE script_id = ANY(batch_script_ids);
END;
$$ LANGUAGE plpgsql;

-- Insert sample data for testing
INSERT INTO lessons (lesson_id, title, subject, grade_level, original_content, source_type) VALUES
('math_algebra_01', 'Introduction to Algebra', 'Mathematics', '9', 'Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols.', 'manual'),
('physics_motion_01', 'Basic Physics: Motion', 'Physics', '10', 'Motion is the change in position of an object with respect to time.', 'manual');

INSERT INTO video_queue (lesson_id, lesson_title, script_id, script_type, content, hook_text, target_platform, priority, adhd_optimized, estimated_attention_span) VALUES
('math_algebra_01', 'Introduction to Algebra', 'math_alg_01_short_1', 'short', 'Hook: Think math is just numbers? Think again! Algebra lets you solve puzzles with letters. In 30 seconds, I''ll show you how x can help you find hidden treasures!', 'Think math is just numbers?', 'tiktok', 1, true, 30),
('math_algebra_01', 'Introduction to Algebra', 'math_alg_01_short_2', 'short', 'Quick tip: Algebra is like a mystery game. x is your missing piece. Want to know how to find x every time? Watch this!', 'Quick tip: Algebra is like a mystery game', 'youtube_shorts', 1, true, 45),
('physics_motion_01', 'Basic Physics: Motion', 'physics_motion_01_short_1', 'short', 'Hook: Why do you feel pushed back when a car starts moving? It''s physics! Motion isn''t just movement - it''s a force story. Let me explain in 30 seconds!', 'Why do you feel pushed back?', 'instagram_reels', 1, true, 30);