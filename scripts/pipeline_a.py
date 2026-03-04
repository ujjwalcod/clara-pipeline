"""
pipeline_a.py – Pipeline A: Demo Call → v1 Account Memo + Retell Agent Spec

Usage:
    python -m scripts.pipeline_a --input data/demo/acme_demo.txt
    python -m scripts.pipeline_a --input data/demo/acme_demo.txt --account-id acme_fire
"""

import argparse
import sys
import traceback
from pathlib import Path

from scripts.extract_memo   import extract_memo
from scripts.generate_agent import generate_agent_spec
from scripts.storage        import save_memo, save_agent_spec, load_memo
from scripts.task_tracker   import create_issue


def run(input_path: str | Path, account_id_override: str | None = None) -> dict:
    """
    Run Pipeline A on a single demo transcript file.

    Returns a result summary dict.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    print(f"\n{'='*60}")
    print(f"Pipeline A  │  {input_path.name}")
    print(f"{'='*60}")

    # ── 1. Read transcript ──────────────────────────────────────────
    transcript = input_path.read_text(encoding="utf-8")
    print(f"  [read]    {len(transcript):,} chars loaded")

    # ── 2. Extract Account Memo ─────────────────────────────────────
    memo = extract_memo(transcript, source_label=input_path.name)
    if account_id_override:
        memo["account_id"] = account_id_override

    account_id = memo["account_id"]
    print(f"  [extract] account_id = {account_id}")

    # ── 3. Check idempotency – skip if v1 already exists ───────────
    existing = load_memo(account_id, "v1")
    if existing:
        print(f"  [skip]    v1 memo already exists for {account_id}. Overwriting.")

    # ── 4. Save v1 memo ─────────────────────────────────────────────
    save_memo(account_id, memo, "v1")

    # ── 5. Generate Retell Agent Spec ───────────────────────────────
    agent_spec = generate_agent_spec(memo, version="v1")
    save_agent_spec(account_id, agent_spec, "v1")

    # ── 6. Create task tracker item ─────────────────────────────────
    create_issue(
        account_id   = account_id,
        company_name = memo.get("company_name", account_id),
        version      = "v1",
        summary      = memo.get("notes", "Demo call processed."),
    )

    result = {
        "status":     "success",
        "account_id": account_id,
        "version":    "v1",
        "input":      str(input_path),
    }
    print(f"\n  ✅ Pipeline A complete for {account_id}")
    return result


# ── CLI entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline A: Demo Call → v1 Agent")
    parser.add_argument("--input",      required=True,  help="Path to transcript file")
    parser.add_argument("--account-id", required=False, help="Override account_id")
    args = parser.parse_args()

    try:
        result = run(args.input, args.account_id)
        print(f"\nResult: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
