"""
diff_patch.py – Merge onboarding data into a v1 memo to produce v2.
Tracks every change in a structured changelog.
"""

import json
from copy import deepcopy
from datetime import datetime, timezone
from scripts.llm_client import call_llm, parse_json_response


_MERGE_SYSTEM = """
You are a data merging assistant for Clara Answers.

You will receive:
1. A v1 Account Memo (derived from a demo call – may have gaps or assumptions)
2. An onboarding update object (confirmed, precise operational data)

Your job:
- Merge the onboarding data INTO the v1 memo to produce a complete v2 memo.
- Only update fields that the onboarding data explicitly addresses.
- Do NOT remove fields that are still valid and unchanged.
- Do NOT hallucinate new fields.
- If there is a conflict between v1 and onboarding, the onboarding data WINS.
- Produce a changelog array that lists every field that changed.

Return a single JSON object with this exact structure:
{
  "v2_memo": { ... complete updated memo ... },
  "changelog": {
    "summary": "<one-sentence description of what changed>",
    "changes": [
      {
        "field": "<JSON path, e.g. business_hours.timezone>",
        "old_value": "<v1 value>",
        "new_value": "<v2 value>",
        "reason": "<why it changed>"
      }
    ],
    "unresolved_conflicts": ["<list any conflicts that need human review>"]
  }
}
"""


def merge_onboarding(v1_memo: dict, onboarding_memo: dict, source_label: str = "") -> tuple[dict, dict]:
    """
    Merge onboarding data into v1 memo.

    Returns:
        (v2_memo, changelog_dict)
    """
    user_prompt = f"""
## V1 Memo (from demo call)
{json.dumps(v1_memo, indent=2)}

## Onboarding Update Data
{json.dumps(onboarding_memo, indent=2)}

Merge them now and return the JSON.
"""
    print(f"  [diff_patch] Merging onboarding data for account: {v1_memo.get('account_id','?')}")
    raw    = call_llm(_MERGE_SYSTEM, user_prompt, expect_json=True)
    result = parse_json_response(raw)

    v2_memo   = result.get("v2_memo", {})
    changelog = result.get("changelog", {})

    # Ensure version markers
    v2_memo["_version"] = "v2"
    v1_memo.setdefault("_version", "v1")

    changelog["account_id"]  = v1_memo.get("account_id", "")
    changelog["source"]      = source_label or "onboarding_call"
    changelog["updated_at"]  = datetime.now(timezone.utc).isoformat()

    return v2_memo, changelog


def simple_diff(v1: dict, v2: dict, path: str = "") -> list[dict]:
    """
    Lightweight recursive diff for display purposes (no LLM needed).
    Returns a flat list of {field, old_value, new_value}.
    """
    changes = []
    all_keys = set(v1.keys()) | set(v2.keys())
    for key in sorted(all_keys):
        full_path = f"{path}.{key}" if path else key
        v1_val    = v1.get(key)
        v2_val    = v2.get(key)
        if isinstance(v1_val, dict) and isinstance(v2_val, dict):
            changes.extend(simple_diff(v1_val, v2_val, full_path))
        elif v1_val != v2_val:
            changes.append({
                "field":     full_path,
                "old_value": v1_val,
                "new_value": v2_val,
            })
    return changes
