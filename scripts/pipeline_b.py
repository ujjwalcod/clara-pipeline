"""
pipeline_b.py – Pipeline B: Onboarding Input → v2 Updated Memo + Agent Spec + Changelog

Usage:
    python -m scripts.pipeline_b --input data/onboarding/acme_onboarding.txt --account-id acme_fire
    python -m scripts.pipeline_b --input data/onboarding/acme_onboarding.txt
       (account_id is inferred from onboarding transcript if not provided)
"""

import argparse
import sys
import traceback
from pathlib import Path

from scripts.extract_memo   import extract_memo
from scripts.generate_agent import generate_agent_spec
from scripts.diff_patch     import merge_onboarding
from scripts.storage        import (
    save_memo, save_agent_spec, save_changelog,
    load_memo, load_agent_spec,
)
from scripts.task_tracker   import create_issue


def run(input_path: str | Path, account_id_override: str | None = None) -> dict:
    """
    Run Pipeline B on a single onboarding transcript.

    Returns a result summary dict.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    print(f"\n{'='*60}")
    print(f"Pipeline B  │  {input_path.name}")
    print(f"{'='*60}")

    # ── 1. Read onboarding transcript ───────────────────────────────
    transcript = input_path.read_text(encoding="utf-8")
    print(f"  [read]    {len(transcript):,} chars loaded")

    # ── 2. Extract onboarding memo (partial – only confirmed fields) ─
    onboarding_memo = extract_memo(transcript, source_label=input_path.name)
    if account_id_override:
        onboarding_memo["account_id"] = account_id_override

    account_id = onboarding_memo.get("account_id", "")

    # ── 3. Load existing v1 memo ────────────────────────────────────
    v1_memo = load_memo(account_id, "v1")
    if not v1_memo:
        print(f"  ⚠️  No v1 memo found for '{account_id}'.")
        print(f"      Running Pipeline A first to create v1...")
        # Auto-create v1 from onboarding (graceful degradation)
        from scripts.pipeline_a import run as run_a
        run_a(input_path, account_id_override=account_id)
        v1_memo = load_memo(account_id, "v1")
        if not v1_memo:
            raise RuntimeError(f"Could not create v1 memo for {account_id}")

    print(f"  [load]    v1 memo loaded for {account_id}")

    # ── 4. Merge onboarding data → produce v2 memo + changelog ──────
    v2_memo, changelog = merge_onboarding(
        v1_memo         = v1_memo,
        onboarding_memo = onboarding_memo,
        source_label    = input_path.name,
    )

    # ── 5. Save v2 memo ─────────────────────────────────────────────
    save_memo(account_id, v2_memo, "v2")

    # ── 6. Generate v2 agent spec ────────────────────────────────────
    agent_spec_v2 = generate_agent_spec(v2_memo, version="v2")
    save_agent_spec(account_id, agent_spec_v2, "v2")

    # ── 7. Save changelog ────────────────────────────────────────────
    save_changelog(account_id, changelog)

    num_changes = len(changelog.get("changes", []))
    print(f"  [diff]    {num_changes} field(s) changed from v1 → v2")

    # ── 8. Update task tracker ───────────────────────────────────────
    create_issue(
        account_id   = account_id,
        company_name = v2_memo.get("company_name", account_id),
        version      = "v2",
        summary      = changelog.get("summary", f"{num_changes} fields updated from onboarding."),
    )

    result = {
        "status":      "success",
        "account_id":  account_id,
        "version":     "v2",
        "input":       str(input_path),
        "num_changes": num_changes,
        "changelog":   changelog.get("summary", ""),
    }
    print(f"\n  ✅ Pipeline B complete for {account_id}")
    return result


# ── CLI entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline B: Onboarding → v2 Agent")
    parser.add_argument("--input",      required=True,  help="Path to onboarding transcript")
    parser.add_argument("--account-id", required=False, help="Override account_id")
    args = parser.parse_args()

    try:
        result = run(args.input, args.account_id)
        print(f"\nResult: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
