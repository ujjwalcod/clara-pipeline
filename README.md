# Clara Answers – Automation Pipeline



VIDEO LINK:
https://www.loom.com/share/03833377d20d48f38c24ea4de1f7b34f

<img width="1914" height="907" alt="image" src="https://github.com/user-attachments/assets/ca7cb98d-6294-4749-a4fe-d30e5f5662a4" />



> **Demo Call → Agent v1 → Onboarding → Agent v2**  
> A zero-cost, reproducible pipeline that converts call transcripts into deployable Retell AI voice agent configurations.

---

## Architecture & Data Flow

```
data/demo/*.txt
      │
      ▼
┌─────────────────────────────────────────────┐
│  PIPELINE A                                 │
│                                             │
│  1. Read transcript                         │
│  2. LLM Extraction  ──► Account Memo v1     │
│  3. Agent Generator ──► Agent Spec v1       │
│  4. Save to outputs/accounts/<id>/v1/       │
│  5. Create GitHub Issue (task tracker)      │
└─────────────────────────────────────────────┘
      │
      ▼
data/onboarding/*.txt
      │
      ▼
┌─────────────────────────────────────────────┐
│  PIPELINE B                                 │
│                                             │
│  1. Read onboarding transcript              │
│  2. LLM Extraction  ──► Onboarding Memo     │
│  3. Load v1 Memo                            │
│  4. LLM Merge       ──► Account Memo v2     │
│  5. Agent Generator ──► Agent Spec v2       │
│  6. Save to outputs/accounts/<id>/v2/       │
│  7. Save changelog.json + changelog.md      │
│  8. Update GitHub Issue                     │
└─────────────────────────────────────────────┘
```

### Output Structure per Account

```
outputs/accounts/<account_id>/
├── v1/
│   ├── memo.json          # Account Memo (demo-derived)
│   └── agent_spec.json    # Retell Agent Draft Spec (v1)
└── v2/
    ├── memo.json          # Account Memo (onboarding-confirmed)
    ├── agent_spec.json    # Retell Agent Draft Spec (v2)
    ├── changelog.json     # Machine-readable diff
    └── changelog.md       # Human-readable diff
```

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourname/clara-pipeline.git
cd clara-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env and add your API key (Groq or Gemini – both free)
```

**Getting a free Groq API key (recommended):**
1. Go to https://console.groq.com
2. Sign up (no credit card needed)
3. Create an API key
4. Paste it as `GROQ_API_KEY` in `.env`

**Getting a free Gemini API key (alternative):**
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Paste it as `GEMINI_API_KEY` in `.env` and set `LLM_PROVIDER=gemini`

### 4. Add your dataset files

Place transcripts in:
```
data/demo/          # demo call transcripts  (*.txt)
data/onboarding/    # onboarding transcripts (*.txt)
```

**Naming convention:** Files are matched by stem. `acme.txt` in demo pairs with `acme.txt` in onboarding.  
Also works with suffixed names: `acme_demo.txt` matches `acme_onboarding.txt`.

---

## Running the Pipeline

### Run a single demo call (Pipeline A)

```bash
python -m scripts.pipeline_a --input data/demo/apex_fire.txt
```

### Run a single onboarding update (Pipeline B)

```bash
python -m scripts.pipeline_b --input data/onboarding/apex_fire.txt
```

### Run all 10 files (batch mode)

```bash
python -m scripts.batch_run
```

### View diff between v1 and v2

```bash
python -m scripts.diff_viewer --account apex_fire
python -m scripts.diff_viewer --account apex_fire --format json
```

---

## Running with n8n (Webhook Mode)

### Start n8n locally with Docker

```bash
docker-compose up -d
```

n8n will be available at: http://localhost:5678

### Import workflows

1. Open http://localhost:5678
2. Go to **Settings → Import Workflow**
3. Import `workflows/n8n_pipeline_a.json`
4. Add your Groq API key to n8n credentials
5. Activate the workflow

### Trigger via webhook

```bash
# Pipeline A
curl -X POST http://localhost:5678/webhook/pipeline-a \
  -H "Content-Type: application/json" \
  -d '{"transcript": "...your transcript text...", "account_id": "acme_fire"}'

# Pipeline B
curl -X POST http://localhost:5678/webhook/pipeline-b \
  -H "Content-Type: application/json" \
  -d '{"transcript": "...onboarding transcript...", "account_id": "acme_fire"}'
```

---

## Retell Integration

### Free Tier Limitation
Retell's free tier does not support programmatic agent creation via API.

### Manual Import Steps
1. Open https://app.retell.ai
2. Create a new agent
3. Copy the `system_prompt` from your generated `agent_spec.json`
4. Paste it into the agent's system prompt field
5. Configure voice using the `voice_style` field
6. Set up call transfer tools using the `tool_invocation_placeholders`
7. Save the agent

### If Retell API Access Becomes Available
Set `RETELL_API_KEY` in `.env`. The pipeline already generates a spec that maps 1:1 to Retell's agent configuration schema.

---

## LLM Options (All Zero-Cost)

| Provider | Free Tier | Model | Setup |
|----------|-----------|-------|-------|
| **Groq** (recommended) | Generous free tier, ~6000 tokens/min | llama-3.3-70b | https://console.groq.com |
| **Gemini Flash** | 15 req/min, 1M tokens/day | gemini-1.5-flash | https://aistudio.google.com |
| **Ollama** | Fully local, unlimited | llama3.2 | https://ollama.com |

Switch provider: `LLM_PROVIDER=groq|gemini|ollama` in `.env`

---
##retell.ai
 Create a free account at **https://app.retell.ai**
Retell Manual Import

   - Open app.retell.ai → Create Agent
   - Copy `system_prompt` from `agent_spec.json`
   - Paste into the agent's system prompt field
   - Set voice to "professional warm"
   - Configure transfer number from `key_variables.emergency_contacts`
   - Save and test

## Known Limitations

- **Audio transcription:** This pipeline accepts text transcripts. If given audio files, use OpenAI Whisper locally (`pip install openai-whisper`) and run `whisper audio.mp3 --output_format txt` first.
- **Retell API:** Free tier does not support programmatic agent creation. Manual import steps are documented above.
- **n8n file writes:** The n8n workflow uses webhook triggers; file I/O in n8n requires appropriate node configuration for your environment.
- **Rate limits:** Groq free tier has rate limits. For batch processing of 10 files, the pipeline runs sequentially to avoid hitting limits.

---

## What I Would Improve With Production Access

1. **Retell API:** Use `POST /create-agent` to automatically create/update agents programmatically
2. **Webhooks from Retell:** Listen for call completion events to auto-trigger Pipeline A
3. **Vector DB (Pinecone/Supabase pgvector):** Store memo embeddings for semantic search across accounts
4. **Whisper API / Deepgram:** Automatic transcription from audio files in the workflow
5. **Slack notifications:** Ping on-call team when a new v2 agent is ready for review
6. **Conflict resolution UI:** A simple web dashboard for reviewing `questions_or_unknowns` fields
7. **A/B testing framework:** Run two agent prompts on test calls and compare outcomes

---

## File Structure

```
clara-pipeline/
├── .env.example              # Environment variable template
├── docker-compose.yml        # n8n local setup
├── requirements.txt
├── README.md
├── data/
│   ├── demo/                 # Place demo transcripts here
│   └── onboarding/           # Place onboarding transcripts here
├── prompts/
│   ├── extraction_prompt.txt # System prompt for memo extraction
│   └── agent_prompt.txt      # System prompt for agent spec generation
├── scripts/
│   ├── config.py             # Central config & env vars
│   ├── llm_client.py         # Groq / Gemini / Ollama abstraction
│   ├── extract_memo.py       # Transcript → Account Memo JSON
│   ├── generate_agent.py     # Account Memo → Retell Agent Spec
│   ├── diff_patch.py         # v1 + onboarding → v2 + changelog
│   ├── storage.py            # Read/write versioned outputs
│   ├── task_tracker.py       # GitHub Issues integration
│   ├── pipeline_a.py         # Pipeline A orchestrator
│   ├── pipeline_b.py         # Pipeline B orchestrator
│   ├── batch_run.py          # Batch processor for all 10 files
│   └── diff_viewer.py        # CLI diff viewer
├── workflows/
│   └── n8n_pipeline_a.json   # n8n workflow export
└── outputs/
    └── accounts/             # Generated per-account outputs
```
