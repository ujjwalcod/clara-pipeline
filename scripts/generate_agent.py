"""
generate_agent.py – Generate a Retell Agent Draft Spec from an Account Memo.
"""

import json
from pathlib import Path
from scripts.config import PROMPTS_DIR
from scripts.llm_client import call_llm, parse_json_response

_AGENT_PROMPT = (PROMPTS_DIR / "agent_prompt.txt").read_text()


def generate_agent_spec(memo: dict, version: str = "v1") -> dict:
    """
    Given an Account Memo dict, produce a Retell Agent Draft Spec dict.

    Args:
        memo:    Account Memo as returned by extract_memo().
        version: "v1" for demo-derived, "v2" for onboarding-updated.

    Returns:
        Retell Agent Spec as a Python dict.
    """
    user_prompt = f"""
Here is the Account Memo to build the agent spec from:

{json.dumps(memo, indent=2)}

Generate the Retell Agent Draft Spec JSON now.
Set the version field to "{version}".
"""
    company = memo.get("company_name", "Unknown")
    print(f"  [generate_agent] Building agent spec for: {company} ({version})")
    raw  = call_llm(_AGENT_PROMPT, user_prompt, expect_json=True)
    spec = parse_json_response(raw)
    spec["version"] = version
    return spec
