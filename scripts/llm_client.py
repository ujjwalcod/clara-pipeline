"""
llm_client.py – Zero-cost LLM abstraction layer.
Supports: Groq (free tier) | Gemini Flash (free tier) | Ollama (local).
"""

import json, requests
from scripts.config import (
    LLM_PROVIDER,
    GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL,
    GEMINI_API_KEY, GEMINI_MODEL, GEMINI_API_URL,
    OLLAMA_HOST, OLLAMA_MODEL,
)


def call_llm(system_prompt: str, user_prompt: str, expect_json: bool = True) -> str:
    """
    Call the configured LLM provider.
    Returns the raw text response (caller parses JSON if needed).
    """
    if LLM_PROVIDER == "groq":
        return _groq(system_prompt, user_prompt)
    elif LLM_PROVIDER == "gemini":
        return _gemini(system_prompt, user_prompt)
    elif LLM_PROVIDER == "ollama":
        return _ollama(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")


# ── Groq (free tier – llama-3.3-70b) ─────────────────────────────────────
def _groq(system_prompt: str, user_prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 4096,
    }
    resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ── Google Gemini Flash (free tier – 15 req/min) ──────────────────────────
def _gemini(system_prompt: str, user_prompt: str) -> str:
    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}
        ],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 4096},
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


# ── Ollama (fully local – no cost at all) ─────────────────────────────────
def _ollama(system_prompt: str, user_prompt: str) -> str:
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "stream": False,
        "options": {"temperature": 0.1},
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def parse_json_response(raw: str) -> dict:
    """Strip markdown fences and parse JSON safely."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        cleaned = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Try to find JSON object in the response
        start = cleaned.find("{")
        end   = cleaned.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(cleaned[start:end])
        raise ValueError(f"Could not parse JSON from LLM response: {e}\nRaw:\n{raw[:500]}")
