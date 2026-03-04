"""
extract_memo.py – Extract structured Account Memo JSON from a transcript.
"""

import json
from pathlib import Path
from scripts.config import PROMPTS_DIR
from scripts.llm_client import call_llm, parse_json_response

_EXTRACTION_PROMPT = (PROMPTS_DIR / "extraction_prompt.txt").read_text()


def extract_memo(transcript: str, source_label: str = "") -> dict:
    """
    Given a raw transcript string, return a structured Account Memo dict.

    Args:
        transcript:   Raw text of the call transcript.
        source_label: Human-readable label for logging (e.g. filename).

    Returns:
        Parsed Account Memo as a Python dict.
    """
    user_prompt = f"""
Here is the call transcript to extract from:

--- TRANSCRIPT START ---
{transcript}
--- TRANSCRIPT END ---

Extract the Account Memo JSON now. Remember: only what is explicitly stated.
"""
    print(f"  [extract_memo] Calling LLM for: {source_label or 'transcript'}")
    raw = call_llm(_EXTRACTION_PROMPT, user_prompt, expect_json=True)
    memo = parse_json_response(raw)

    # Normalise account_id: lowercase, underscores, no special chars
    if memo.get("company_name") and not memo.get("account_id"):
        memo["account_id"] = _slugify(memo["company_name"])

    return memo


def _slugify(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
