# Feature: Daily Market Research Cron Job (Agent-Powered)

The following plan should be complete, but its important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Fully automated daily competitor and market research system that:
1. Runs on a schedule via Supabase pg_cron (8am daily)
2. Uses Tavily API to research competitors and industry trends
3. Stores raw intelligence in Supabase `market_intel` table
4. **Calls Marketing Agent to digest and analyze the data**
5. Agent creates actionable insights using business context
6. Agent sends personalized digest to Slack #market-intel

**Key Differentiator**: The agent digests raw research into actionable marketing insights, not just raw data dumps.

## User Story

As a **marketing team member**
I want to **receive daily competitor intelligence and market trends automatically**
So that **I can create timely, relevant content and stay ahead of competitors**

## Problem Statement

Marketing teams need fresh competitive intelligence to create relevant content, but manually researching competitors daily is time-consuming and often forgotten. The marketing agent also lacks current market context when generating content.

## Solution Statement

Create an automated pipeline using Supabase Edge Functions + pg_cron that:
- Researches configured competitors via Tavily API daily
- Stores findings in a database table the agent can query
- Delivers actionable digest to Slack for the marketing team

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Medium
**Primary Systems Affected**: Supabase (Edge Functions, pg_cron, Database), Slack
**Dependencies**: Tavily API, Slack Incoming Webhook, Supabase CLI

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `server/db/supabase.py` (lines 1-27) - Why: Shows Supabase client pattern used in project
- `server/agent/memory.py` (lines 1-50) - Why: Database table patterns and error handling
- `server/slack_bot.py` (lines 1-50) - Why: Slack integration patterns
- `deploy-slack-bot/slack_bot.py` - Why: Environment variable patterns for Slack

### New Files to Create

- `supabase/functions/daily-market-research/index.ts` - Edge Function for research
- `supabase/functions/_shared/tavily.ts` - Tavily client wrapper
- `supabase/functions/_shared/slack.ts` - Slack webhook helper
- `supabase/migrations/20260120_market_intel_table.sql` - Database table
- `supabase/migrations/20260120_market_research_cron.sql` - Cron job setup
- `.claude/skills/business-profile/SKILL.md` - Business context for agent

### Relevant Documentation YOU SHOULD READ THESE BEFORE IMPLEMENTING!

- [Supabase Edge Functions Guide](https://supabase.com/docs/guides/functions)
  - Specific section: Quickstart and deployment
  - Why: Core deployment pattern
- [Supabase pg_cron + Edge Functions](https://supabase.com/docs/guides/functions/schedule-functions)
  - Specific section: Scheduling with pg_net
  - Why: Shows exact pattern for cron → edge function
- [Tavily SDK Reference](https://docs.tavily.com/sdk/javascript/reference)
  - Specific section: Search options
  - Why: API parameters for research queries
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
  - Why: Design rich message format

### Patterns to Follow

**Supabase Table Pattern (from memory.py):**
```python
try:
    self.client.table("table_name").insert({
        "column": value
    }).execute()
except Exception as e:
    logger.error(f"Failed to operation: {e}")
    raise RuntimeError(f"Database error: {e}")
```

**Environment Variables Pattern:**
- Use `Deno.env.get('VAR_NAME')` in Edge Functions
- Store secrets in Supabase Vault for cron jobs

**Error Handling:**
- Log errors with context
- Return graceful error responses
- Don't expose internal details

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation

- Set up Supabase CLI and link project
- Create database table for market intelligence
- Create business profile skill for agent context
- Get API keys (Tavily, Slack webhook)

### Phase 2: Core Implementation

- Create Tavily client wrapper
- Create Slack webhook helper
- Implement main Edge Function
- Add configuration for competitors/keywords

### Phase 3: Integration

- Deploy Edge Function to Supabase
- Set up pg_cron schedule
- Store secrets in Vault
- Update agent to read market_intel table

### Phase 4: Testing & Validation

- Test Edge Function manually
- Verify Slack message formatting
- Confirm cron job triggers correctly
- Test agent context integration

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### Task 1: CREATE Supabase project structure

- **IMPLEMENT**: Initialize Supabase functions directory structure
- **COMMANDS**:
  ```bash
  cd "/Users/blutrich/Documents/DEV/Vibe Marketing Base44"
  mkdir -p supabase/functions/daily-market-research
  mkdir -p supabase/functions/_shared
  mkdir -p supabase/migrations
  ```
- **VALIDATE**: `ls -la supabase/functions/`

---

### Task 2: CREATE market_intel database table

- **IMPLEMENT**: Create migration for market intelligence storage
- **FILE**: `supabase/migrations/20260120_market_intel_table.sql`
- **CONTENT**:
  ```sql
  -- Market Intelligence Table
  -- Stores daily research results for agent context and historical tracking

  CREATE TABLE IF NOT EXISTS market_intel (
      id SERIAL PRIMARY KEY,
      research_date DATE NOT NULL DEFAULT CURRENT_DATE,
      category TEXT NOT NULL, -- 'competitor', 'trend', 'news', 'opportunity'
      source TEXT NOT NULL, -- competitor name or topic
      title TEXT NOT NULL,
      content TEXT NOT NULL,
      url TEXT,
      relevance_score FLOAT DEFAULT 0.0,
      metadata JSONB DEFAULT '{}',
      created_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Index for efficient querying by date and category
  CREATE INDEX idx_market_intel_date ON market_intel(research_date DESC);
  CREATE INDEX idx_market_intel_category ON market_intel(category);

  -- Index for agent queries (recent intel)
  CREATE INDEX idx_market_intel_recent ON market_intel(created_at DESC);

  -- Unique constraint to prevent duplicate entries
  CREATE UNIQUE INDEX idx_market_intel_unique
  ON market_intel(research_date, category, source, title);
  ```
- **VALIDATE**: Run in Supabase SQL Editor or via CLI

---

### Task 3: CREATE business-profile skill

- **IMPLEMENT**: Create permanent business context for agent
- **FILE**: `.claude/skills/business-profile/SKILL.md`
- **CONTENT**:
  ```markdown
  # Business Profile

  ## Company Information
  - **Company**: [TO BE FILLED BY USER]
  - **Industry**: AI Consulting / Technology
  - **Location**: Israel
  - **Languages**: Hebrew, English

  ## What We Do
  [Description of services - TO BE FILLED]

  ## Target Audience
  - Enterprise decision makers
  - CTOs and technology leaders
  - Companies implementing AI solutions

  ## Brand Voice
  - Professional but approachable
  - Data-driven with specific examples
  - Avoid jargon, explain concepts clearly
  - Bilingual (Hebrew and English)

  ## Competitors to Monitor
  - [Competitor 1 - TO BE FILLED]
  - [Competitor 2 - TO BE FILLED]
  - [Competitor 3 - TO BE FILLED]

  ## Industry Keywords
  - AI implementation
  - Enterprise AI
  - Digital transformation
  - AI ROI

  ## Content Guidelines
  - Always include actionable takeaways
  - Use real examples and case studies
  - Preferred hashtags: #AI #Enterprise #DigitalTransformation

  ## Market Intelligence
  When creating content, check the `market_intel` table for:
  - Recent competitor announcements
  - Trending industry topics
  - Content opportunities and gaps

  Query example:
  ```sql
  SELECT * FROM market_intel
  WHERE research_date >= CURRENT_DATE - INTERVAL '7 days'
  ORDER BY created_at DESC;
  ```
  ```
- **VALIDATE**: `cat .claude/skills/business-profile/SKILL.md`

---

### Task 4: CREATE Tavily client wrapper

- **IMPLEMENT**: Reusable Tavily search client
- **FILE**: `supabase/functions/_shared/tavily.ts`
- **CONTENT**:
  ```typescript
  // Tavily API client wrapper for market research

  interface TavilySearchOptions {
    searchDepth?: "basic" | "advanced";
    maxResults?: number;
    includeAnswer?: boolean;
    topic?: "general" | "news" | "finance";
  }

  interface TavilyResult {
    title: string;
    url: string;
    content: string;
    score: number;
  }

  interface TavilyResponse {
    query: string;
    results: TavilyResult[];
    answer?: string;
    responseTime: number;
  }

  export async function searchTavily(
    query: string,
    options: TavilySearchOptions = {}
  ): Promise<TavilyResponse> {
    const apiKey = Deno.env.get("TAVILY_API_KEY");
    if (!apiKey) {
      throw new Error("TAVILY_API_KEY not configured");
    }

    const response = await fetch("https://api.tavily.com/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        api_key: apiKey,
        query,
        search_depth: options.searchDepth || "advanced",
        max_results: options.maxResults || 5,
        include_answer: options.includeAnswer ?? true,
        topic: options.topic || "news",
      }),
    });

    if (!response.ok) {
      throw new Error(`Tavily API error: ${response.statusText}`);
    }

    return await response.json();
  }

  export async function researchCompetitor(
    competitorName: string
  ): Promise<TavilyResponse> {
    return searchTavily(
      `${competitorName} company news announcements updates`,
      { searchDepth: "advanced", maxResults: 3, topic: "news" }
    );
  }

  export async function researchTrend(
    keyword: string
  ): Promise<TavilyResponse> {
    return searchTavily(
      `${keyword} trends news 2026`,
      { searchDepth: "advanced", maxResults: 3, topic: "news" }
    );
  }
  ```
- **VALIDATE**: TypeScript syntax check

---

### Task 5: CREATE Slack webhook helper

- **IMPLEMENT**: Reusable Slack message sender
- **FILE**: `supabase/functions/_shared/slack.ts`
- **CONTENT**:
  ```typescript
  // Slack webhook helper for sending formatted messages

  interface SlackBlock {
    type: string;
    text?: {
      type: string;
      text: string;
      emoji?: boolean;
    };
    elements?: any[];
    accessory?: any;
  }

  interface SlackMessage {
    text: string;
    blocks?: SlackBlock[];
  }

  export async function sendSlackMessage(
    message: SlackMessage
  ): Promise<boolean> {
    const webhookUrl = Deno.env.get("SLACK_WEBHOOK_URL");
    if (!webhookUrl) {
      throw new Error("SLACK_WEBHOOK_URL not configured");
    }

    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    });

    return response.ok;
  }

  export function formatMarketIntelMessage(
    competitors: Array<{ name: string; findings: string[] }>,
    trends: Array<{ topic: string; summary: string }>,
    opportunities: string[]
  ): SlackMessage {
    const blocks: SlackBlock[] = [
      {
        type: "header",
        text: {
          type: "plain_text",
          text: "📊 Daily Market Intelligence",
          emoji: true,
        },
      },
      {
        type: "context",
        elements: [
          {
            type: "mrkdwn",
            text: `*Date:* ${new Date().toLocaleDateString("en-IL")}`,
          },
        ],
      },
      { type: "divider" },
    ];

    // Competitor section
    if (competitors.length > 0) {
      blocks.push({
        type: "section",
        text: {
          type: "mrkdwn",
          text: "*🎯 COMPETITOR MOVES*",
        },
      });

      competitors.forEach((comp) => {
        const findings = comp.findings.map((f) => `• ${f}`).join("\n");
        blocks.push({
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*${comp.name}*\n${findings}`,
          },
        });
      });

      blocks.push({ type: "divider" });
    }

    // Trends section
    if (trends.length > 0) {
      blocks.push({
        type: "section",
        text: {
          type: "mrkdwn",
          text: "*📈 TRENDING TOPICS*",
        },
      });

      trends.forEach((trend) => {
        blocks.push({
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*${trend.topic}*\n${trend.summary}`,
          },
        });
      });

      blocks.push({ type: "divider" });
    }

    // Opportunities section
    if (opportunities.length > 0) {
      blocks.push({
        type: "section",
        text: {
          type: "mrkdwn",
          text: "*💡 CONTENT OPPORTUNITIES*",
        },
      });

      blocks.push({
        type: "section",
        text: {
          type: "mrkdwn",
          text: opportunities.map((o) => `• ${o}`).join("\n"),
        },
      });
    }

    return {
      text: "Daily Market Intelligence Report",
      blocks,
    };
  }
  ```
- **VALIDATE**: TypeScript syntax check

---

### Task 6: CREATE main Edge Function (Agent-Powered)

- **IMPLEMENT**: Daily market research with agent digestion
- **FILE**: `supabase/functions/daily-market-research/index.ts`
- **CONTENT**:
  ```typescript
  // Daily Market Research Edge Function (Agent-Powered)
  // 1. Fetches research via Tavily
  // 2. Stores in database
  // 3. Calls Agent to digest and send to Slack

  import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
  import { searchTavily, researchCompetitor, researchTrend } from "../_shared/tavily.ts";

  // Configuration - can be moved to database or environment
  const CONFIG = {
    competitors: [
      "OpenAI",
      "Anthropic",
      "Google AI",
      // Add your actual competitors here
    ],
    keywords: [
      "AI implementation enterprise",
      "AI consulting services",
      "digital transformation AI",
    ],
  };

  interface MarketIntelRecord {
    research_date: string;
    category: string;
    source: string;
    title: string;
    content: string;
    url: string | null;
    relevance_score: number;
    metadata: Record<string, any>;
  }

  Deno.serve(async (req) => {
    try {
      console.log("Starting daily market research...");

      // Initialize Supabase client
      const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
      const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
      const supabase = createClient(supabaseUrl, supabaseKey);

      const agentApiUrl = Deno.env.get("AGENT_API_URL")!;
      const slackWebhookUrl = Deno.env.get("SLACK_WEBHOOK_URL")!;

      const today = new Date().toISOString().split("T")[0];
      const records: MarketIntelRecord[] = [];

      // ========== STEP 1: Research via Tavily ==========
      console.log("Researching competitors...");
      for (const competitor of CONFIG.competitors) {
        try {
          const result = await researchCompetitor(competitor);
          for (const item of result.results) {
            records.push({
              research_date: today,
              category: "competitor",
              source: competitor,
              title: item.title,
              content: item.content,
              url: item.url,
              relevance_score: item.score,
              metadata: { query: result.query },
            });
          }
        } catch (error) {
          console.error(`Error researching ${competitor}:`, error);
        }
      }

      console.log("Researching trends...");
      for (const keyword of CONFIG.keywords) {
        try {
          const result = await researchTrend(keyword);
          for (const item of result.results) {
            records.push({
              research_date: today,
              category: "trend",
              source: keyword,
              title: item.title,
              content: item.content,
              url: item.url,
              relevance_score: item.score,
              metadata: { query: result.query, answer: result.answer },
            });
          }
        } catch (error) {
          console.error(`Error researching trend ${keyword}:`, error);
        }
      }

      // ========== STEP 2: Store in Database ==========
      console.log(`Storing ${records.length} records...`);
      if (records.length > 0) {
        const { error: insertError } = await supabase
          .from("market_intel")
          .upsert(records, {
            onConflict: "research_date,category,source,title",
            ignoreDuplicates: true,
          });

        if (insertError) {
          console.error("Database insert error:", insertError);
        }
      }

      // ========== STEP 3: Call Agent to Digest ==========
      console.log("Calling agent to digest research...");

      // Build summary for agent
      const competitorSummary = records
        .filter(r => r.category === "competitor")
        .map(r => `- ${r.source}: ${r.title}`)
        .join("\n");

      const trendSummary = records
        .filter(r => r.category === "trend")
        .map(r => `- ${r.source}: ${r.title}`)
        .join("\n");

      const agentPrompt = `
You are preparing the daily market intelligence digest for the marketing team.

## Today's Research (${today})

### Competitor Activity
${competitorSummary || "No competitor news found today."}

### Industry Trends
${trendSummary || "No major trends identified today."}

## Your Task

Analyze this research and create an ACTIONABLE digest for the marketing team. Include:

1. **🎯 Key Competitor Moves** - What competitors did and what it means for us
2. **📈 Trending Opportunities** - Topics we should create content about TODAY
3. **💡 Specific Content Ideas** - 2-3 ready-to-execute post ideas with hooks
4. **⚡ Quick Wins** - One thing the team can do in the next hour

Format this beautifully for Slack. Use emojis, bold text, and clear sections.
Keep it actionable - the team should know exactly what to do after reading this.

After creating the digest, send it to Slack using the webhook.
      `.trim();

      // Call Agent API
      const agentResponse = await fetch(`${agentApiUrl}/agent/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: agentPrompt,
          metadata: {
            task: "daily_market_digest",
            slack_webhook: slackWebhookUrl,
          }
        }),
      });

      const agentResult = await agentResponse.json();
      console.log("Agent response received");

      // ========== STEP 4: Send to Slack ==========
      // The agent should send to Slack, but as backup:
      if (agentResult.content) {
        const slackResponse = await fetch(slackWebhookUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: "📊 Daily Market Intelligence",
            blocks: [
              {
                type: "section",
                text: {
                  type: "mrkdwn",
                  text: agentResult.content.substring(0, 3000), // Slack limit
                },
              },
            ],
          }),
        });
        console.log(`Slack sent: ${slackResponse.ok}`);
      }

      return new Response(
        JSON.stringify({
          success: true,
          records_stored: records.length,
          agent_digest: !!agentResult.content,
        }),
        {
          headers: { "Content-Type": "application/json" },
        }
      );
    } catch (error) {
      console.error("Market research failed:", error);
      return new Response(
        JSON.stringify({ success: false, error: error.message }),
        {
          status: 500,
          headers: { "Content-Type": "application/json" },
        }
      );
    }
  });
  ```
- **VALIDATE**: `deno check supabase/functions/daily-market-research/index.ts`

---

### Task 7: CREATE pg_cron migration

- **IMPLEMENT**: Schedule daily research at 8am Israel time (6am UTC)
- **FILE**: `supabase/migrations/20260120_market_research_cron.sql`
- **CONTENT**:
  ```sql
  -- Enable required extensions
  CREATE EXTENSION IF NOT EXISTS pg_cron WITH SCHEMA pg_catalog;
  CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions;

  -- Store secrets in Vault (run manually in Supabase dashboard)
  -- select vault.create_secret('https://yrjrhiqokjtbtqkgsbjy.supabase.co', 'project_url');
  -- select vault.create_secret('YOUR_SERVICE_ROLE_KEY', 'service_role_key');

  -- Schedule daily market research at 6am UTC (8am Israel)
  SELECT cron.schedule(
    'daily-market-research',
    '0 6 * * *',  -- 6am UTC = 8am Israel time
    $$
    SELECT net.http_post(
      url := (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'project_url')
             || '/functions/v1/daily-market-research',
      headers := jsonb_build_object(
        'Content-Type', 'application/json',
        'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'service_role_key')
      ),
      body := '{}'::jsonb
    ) AS request_id;
    $$
  );

  -- View scheduled jobs
  -- SELECT * FROM cron.job;

  -- Unschedule if needed
  -- SELECT cron.unschedule('daily-market-research');
  ```
- **GOTCHA**: Vault secrets must be created manually in Supabase Dashboard
- **VALIDATE**: Check cron job: `SELECT * FROM cron.job;`

---

### Task 8: DEPLOY Edge Function

- **IMPLEMENT**: Deploy function to Supabase
- **COMMANDS**:
  ```bash
  # Login to Supabase CLI
  supabase login

  # Link to project
  supabase link --project-ref yrjrhiqokjtbtqkgsbjy

  # Deploy function
  supabase functions deploy daily-market-research --no-verify-jwt

  # Set secrets
  supabase secrets set TAVILY_API_KEY=tvly-YOUR_KEY
  supabase secrets set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
  ```
- **VALIDATE**: `supabase functions list`

---

### Task 9: CONFIGURE Vault secrets for cron

- **IMPLEMENT**: Store secrets in Supabase Vault (run in SQL Editor)
- **SQL**:
  ```sql
  -- Store project URL
  SELECT vault.create_secret(
    'https://yrjrhiqokjtbtqkgsbjy.supabase.co',
    'project_url'
  );

  -- Store service role key
  SELECT vault.create_secret(
    'YOUR_SERVICE_ROLE_KEY_HERE',
    'service_role_key'
  );
  ```
- **VALIDATE**: `SELECT name FROM vault.decrypted_secrets;`

---

### Task 10: UPDATE agent to query market_intel

- **IMPLEMENT**: Add market intel context to agent system prompt
- **FILE**: `server/agent/client.py`
- **PATTERN**: Update SYSTEM_PROMPT to include market intel awareness
- **ADD** to system prompt:
  ```python
  """
  ...existing prompt...

  You have access to market intelligence in the database. When creating marketing content,
  consider querying recent competitor moves and industry trends from the market_intel table
  to make content timely and relevant.
  """
  ```
- **VALIDATE**: Restart agent and verify prompt includes market intel reference

---

### Task 11: TEST manual function invocation

- **IMPLEMENT**: Test Edge Function manually
- **COMMAND**:
  ```bash
  curl -X POST \
    'https://yrjrhiqokjtbtqkgsbjy.supabase.co/functions/v1/daily-market-research' \
    -H 'Authorization: Bearer YOUR_SERVICE_ROLE_KEY' \
    -H 'Content-Type: application/json'
  ```
- **VALIDATE**:
  - Check response for success: true
  - Check Slack channel for message
  - Check database: `SELECT COUNT(*) FROM market_intel WHERE research_date = CURRENT_DATE;`

---

## TESTING STRATEGY

### Unit Tests

- Tavily client returns expected response structure
- Slack message formatter produces valid blocks
- Database records have correct schema

### Integration Tests

- Edge Function completes without errors
- Records are stored in database
- Slack message is delivered
- Cron job triggers at scheduled time

### Edge Cases

- Tavily API rate limit or error
- Slack webhook failure
- Empty research results
- Duplicate records (should be handled by upsert)
- Network timeout

---

## VALIDATION COMMANDS

### Level 1: Syntax & Deployment

```bash
# Check TypeScript syntax
deno check supabase/functions/daily-market-research/index.ts

# Deploy and verify
supabase functions deploy daily-market-research
supabase functions list
```

### Level 2: Function Test

```bash
# Manual invocation
curl -X POST \
  'https://yrjrhiqokjtbtqkgsbjy.supabase.co/functions/v1/daily-market-research' \
  -H 'Authorization: Bearer SERVICE_ROLE_KEY' \
  -H 'Content-Type: application/json'
```

### Level 3: Database Verification

```sql
-- Check records
SELECT * FROM market_intel
WHERE research_date = CURRENT_DATE
ORDER BY created_at DESC;

-- Check cron job
SELECT * FROM cron.job WHERE jobname = 'daily-market-research';

-- Check cron execution history
SELECT * FROM cron.job_run_details
WHERE jobname = 'daily-market-research'
ORDER BY start_time DESC
LIMIT 5;
```

### Level 4: Manual Validation

- [ ] Check Slack #market-intel channel for formatted message
- [ ] Verify message contains competitor and trend sections
- [ ] Ask agent about recent competitor moves (should reference market_intel)

---

## ACCEPTANCE CRITERIA

- [ ] Edge Function deploys successfully to Supabase
- [ ] pg_cron job is scheduled for 8am Israel time
- [ ] Tavily API returns competitor research results
- [ ] Results are stored in market_intel table
- [ ] Slack receives formatted daily digest
- [ ] Agent can reference recent market intelligence
- [ ] Duplicate records are handled gracefully
- [ ] Errors are logged but don't crash the function

---

## COMPLETION CHECKLIST

- [ ] Database table created (market_intel)
- [ ] Business profile skill created
- [ ] Tavily client wrapper implemented
- [ ] Slack helper implemented
- [ ] Main Edge Function implemented
- [ ] Function deployed to Supabase
- [ ] Secrets configured (Tavily, Slack webhook)
- [ ] Vault secrets created for cron
- [ ] pg_cron job scheduled
- [ ] Manual test successful
- [ ] Slack message received
- [ ] Agent updated with market intel awareness

---

## NOTES

### Required API Keys

1. **Tavily API Key**: Get free at https://tavily.com (1000 free searches/month)
2. **Slack Webhook URL**: Create at https://api.slack.com → Your App → Incoming Webhooks

### Cost Considerations

- Tavily: Free tier = 1000 searches/month, ~15 searches/day = 450/month
- Supabase: Edge Functions included in free tier
- Slack: Webhooks are free

### Future Enhancements

1. Add configuration UI to update competitors/keywords
2. Add sentiment analysis to research results
3. Create weekly summary in addition to daily
4. Add competitor content similarity detection
5. Integrate with LinkedIn to track competitor posts directly

### Configuration Location

Competitors and keywords are currently hardcoded in the Edge Function CONFIG object. For production, consider:
- Moving to environment variables
- Storing in a `config` table in Supabase
- Reading from business-profile skill

### Timezone Note

Israel timezone is UTC+2 (or UTC+3 during daylight saving). The cron is set for 6am UTC which is 8am Israel Standard Time.
