# Context

I am a data scientist with strong Python skills but 
limited experience with LLMs and AI agents. I am building agents 
on my local machine as a learning exercise. I want to deeply understand what I'm building, not just 
get it working.

# Teaching Approach

- Always explain the *why* and the core concept before implementation
- Use the progression: Fundamentals → Architecture → Tools → Optimisation
- Use analogies for abstract concepts (e.g. memory, reasoning loops)
- When I share code, identify what I've done well before suggesting 
  improvements
- Prefer skeleton code and pseudocode over complete implementations
- Ask me a follow-up question to check my understanding after 
  explaining something non-trivial

# What I'm Learning

Key topics I'm working through:
- Tokenisation, context windows, embeddings
- RAG and vector databases
- Prompt engineering and tool use
- Agent memory and reasoning loops
- Corporate considerations: privacy, cost, scalability

# Preferences

- Use double quotes for all Python strings
- Favour explanations over solutions — I want to understand, 
  not just copy
- When there are multiple valid approaches (e.g. fine-tuning vs RAG), 
  explain the tradeoffs rather than just recommending one
- Keep responses focused — if a topic is deep, offer to go further 
  rather than covering everything at once

# Project

Building a newsletter summarisation agent as a learning exercise. 
The agent will ingest newsletters from a gmail account and produce structured summaries
as well as mp3 files I can listen to on my phone.
Summarisation uses Gemini 2.5 Flash via API; TTS uses edge-tts (local, free).

The primary goal is learning agent architecture through building 
something real and useful, not shipping a production system.

## What I want to understand through this project
- How to structure an ingestion and preprocessing pipeline
- How to prompt effectively for summarisation tasks
- When and whether RAG adds value for this use case
- How to evaluate summary quality

# Hardware

## Main PC
- GPU: 7900xt 20GB VRAM
- RAM: 32GB
- CPU: Ryzen 7 5800X3D
- OS: Windows
- Running models locally via Ollama
- Current models I'm using: qwen2.5-coder:7b

## Home server
- GPU: None
- CPU: i5-7400
- RAM: 16GB

## MacBook (development / Claude Code)
- No local GPU for Ollama
- Used for editing, Claude Code sessions, and pushing to git
- Connects to the Windows PC's Ollama instance via network if needed

# Current Implementation State

## What's built

- `email_tool.py` — connects to Gmail via IMAP, fetches unread emails,
  strips HTML with BeautifulSoup, and truncates at 15,000 chars to protect the context window
- `summarise.py` — makes direct API calls (no agent framework) returning structured JSON
  using `newsletter_system_prompt.md`; routes to Gemini or Ollama based on env vars
- `tts.py` — takes a text string and generates an MP3 using `edge-tts`; outputs to `tts_output/`
- `orchestrator.py` — early experiment using SmolAgents CodeAgent; **now considered abandoned**,
  the decision was made to handle model request routing directly instead
- `newsletter_system_prompt.md` — system prompt for the summarisation task
- `example_json_response_format.json` — target output schema for structured summaries

## Backend switching

`summarise.py` supports two backends via environment variables:
- **Local (Ollama):** no `GEMINI_API_KEY` in `.env` → routes to `http://localhost:11434`
- **Remote (Gemini):** set `GEMINI_API_KEY` and `MODEL=gemini-2.5-flash` → routes to Gemini's OpenAI-compatible endpoint
- Backend is selected automatically — no `MACHINE` variable needed

**Required `.env` variables for Gemini backend:**
```
GEMINI_API_KEY=<your key>
MODEL=gemini-2.5-flash
```

`gemini-2.0-flash` and older models have a free tier quota of 0 — only `gemini-2.5-flash` and
`gemini-2.5-flash-lite` are confirmed free as of 2026-06-06.

This allows development on the MacBook (no local GPU) using Gemini free tier credits.

## What's still TODO

- Wire `email_tool.py` into `summarise.py` to process real emails
- Wire `summarise.py` output (`tts_script` field) into `tts.py` to generate audio
- `main.py` is a placeholder only — needs to become the pipeline entry point
- No scheduling or automation yet (currently run manually)

## Known issues / future work

### Truncated newsletters
Many newsletters truncate body text in the email and require clicking a "read online" link to view the full content. `email_tool.py` will only capture the truncated version. A future web scraping step will be needed to follow the URL and fetch the full article before passing to the summariser.

## Cross-machine workflow

This file is the source of truth for project state across machines (Main PC and MacBook).
Do not suggest syncing the Claude Code memory system — CLAUDE.md is intentionally used instead.
Ask to update this file at the end of any session where something meaningful changes.

## Architecture direction

Handling model routing and orchestration manually (direct API calls) rather than delegating to
an agent framework like SmolAgents. This gives more transparency into what's happening and aligns
with the learning goals. SmolAgents was tried and abandoned — the CodeAgent pattern burned context
on meta-reasoning rather than summarisation, producing poor output with 7B models.

# Last updated

<!-- Format: date | machine | 2-sentence summary of what changed -->

- 2026-06-05 | MacBook — Added Current Implementation State section, hardware entry for MacBook, and this log. Removed stale SmolAgents reference from Context; SmolAgents abandoned in favour of direct Ollama API calls.
- 2026-06-05 | MacBook — Added Cross-machine workflow section documenting the decision to use CLAUDE.md as the memory source of truth instead of syncing Claude Code's memory system.
- 2026-06-05 | MacBook — Added Gemini free tier fallback to summarise.py; backend now switches automatically based on presence of GEMINI_API_KEY in .env. Tested and working.
- 2026-06-05 | MacBook — Simplified backend switching (dropped MACHINE variable); standardised all Python strings to double quotes.
- 2026-06-06 | Main PC — Confirmed gemini-2.5-flash produces quality output (differentiated summary and tts_script). Added TODO for TTS stage (edge-tts) and documented truncated newsletter issue.
- 2026-06-06 | Main PC — Built tts.py using edge-tts; working and producing MP3 output. Documented required .env variables and confirmed gemini-2.5-flash as the only free-tier model that works. Next session: wire email_tool → summarise → tts into main.py.