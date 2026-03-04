"""
diff_viewer.py – Print a colour-coded diff between v1 and v2 for any account.

Usage:
    python -m scripts.diff_viewer --account acme_fire
    python -m scripts.diff_viewer --account acme_fire --format json
"""

import argparse
import json
from scripts.storage    import load_memo, load_agent_spec, list_accounts
from scripts.diff_patch import simple_diff

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def print_diff(account_id: str, output_format: str = "pretty"):
    v1_memo = load_memo(account_id, "v1")
    v2_memo = load_memo(account_id, "v2")

    if not v1_memo:
        print(f"❌ No v1 memo found for account: {account_id}")
        return
    if not v2_memo:
        print(f"⚠️  No v2 memo found for account: {account_id} (onboarding not yet run)")
        return

    changes = simple_diff(v1_memo, v2_memo)

    if output_format == "json":
        print(json.dumps(changes, indent=2))
        return

    # ── Pretty print ────────────────────────────────────────────────
    print(f"\n{BOLD}{CYAN}Diff: {account_id}  (v1 → v2){RESET}")
    print(f"{'─'*60}")

    if not changes:
        print(f"{GREEN}No differences found.{RESET}")
        return

    for change in changes:
        field     = change["field"]
        old_value = change["old_value"]
        new_value = change["new_value"]

        print(f"\n{BOLD}{YELLOW}Field:{RESET} {field}")
        print(f"  {RED}- {json.dumps(old_value)}{RESET}")
        print(f"  {GREEN}+ {json.dumps(new_value)}{RESET}")

    print(f"\n{'─'*60}")
    print(f"{BOLD}Total changes: {len(changes)}{RESET}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View diff between v1 and v2 memo")
    parser.add_argument("--account", required=False, help="Account ID (omit to list all)")
    parser.add_argument("--format",  default="pretty", choices=["pretty", "json"])
    args = parser.parse_args()

    if not args.account:
        accounts = list_accounts()
        if not accounts:
            print("No accounts found in outputs/.")
        else:
            print("Available accounts:")
            for a in accounts:
                print(f"  • {a}")
    else:
        print_diff(args.account, args.format)
