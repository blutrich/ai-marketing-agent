-- Migration: 001_create_agent_tables
-- Description: Create tables for autonomous agent (sessions, content_log, preferences, tasks)

-- Sessions table: Track agent conversation sessions
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  summary TEXT,
  tags TEXT[],
  metadata JSONB DEFAULT '{}'::jsonb
);

-- Content log table: Track all content created by agent
CREATE TABLE IF NOT EXISTS content_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT REFERENCES sessions(session_id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  content_type TEXT NOT NULL,
  platform TEXT,
  title TEXT,
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb,
  performance JSONB DEFAULT '{}'::jsonb
);

-- Preferences table: Store user/brand preferences
CREATE TABLE IF NOT EXISTS preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT UNIQUE NOT NULL,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks table: Track autonomous tasks
CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id TEXT UNIQUE NOT NULL,
  session_id TEXT REFERENCES sessions(session_id) ON DELETE SET NULL,
  goal TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
  progress TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  webhook_url TEXT,
  result JSONB,
  error TEXT,
  cost_usd DECIMAL(10,6) DEFAULT 0
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_log_created_at ON content_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_log_content_type ON content_log(content_type);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(started_at DESC);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to sessions
DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to preferences
DROP TRIGGER IF EXISTS update_preferences_updated_at ON preferences;
CREATE TRIGGER update_preferences_updated_at
    BEFORE UPDATE ON preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
