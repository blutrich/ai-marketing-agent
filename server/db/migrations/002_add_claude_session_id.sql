-- Migration: 002_add_claude_session_id
-- Description: Add claude_session_id column for SDK session persistence

-- Add column to store Anthropic's SDK session ID
ALTER TABLE sessions
ADD COLUMN IF NOT EXISTS claude_session_id TEXT;

-- Index for looking up by Claude session ID
CREATE INDEX IF NOT EXISTS idx_sessions_claude_session_id ON sessions(claude_session_id);

-- Comment
COMMENT ON COLUMN sessions.claude_session_id IS 'Anthropic Claude SDK session ID for resume functionality';
