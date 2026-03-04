"""
config.py – Central config. All secrets come from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")

# ── Paths ──────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent.parent
DATA_DIR    = ROOT / "data"
DEMO_DIR    = DATA_DIR / "demo"
ONBOARD_DIR = DATA_DIR / "onboarding"
OUTPUT_DIR  = ROOT / "outputs" / "accounts"
PROMPTS_DIR = ROOT / "prompts"

# ── LLM Provider ────────────────────────────────────────────────────────
# Options: "groq" | "gemini" | "ollama"
# Groq and Gemini both have free tiers. Ollama is fully local.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL     = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_URL   = "https://api.groq.com/openai/v1/chat/completions"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

OLLAMA_HOST    = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL   = os.getenv("OLLAMA_MODEL", "llama3.2")

# ── GitHub Task Tracker (optional) ──────────────────────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO  = os.getenv("GITHUB_REPO", "")   # e.g. "yourname/clara-pipeline"

# ── Retell (spec only – free tier has no programmatic agent creation) ──
RETELL_API_KEY = os.getenv("RETELL_API_KEY", "")
