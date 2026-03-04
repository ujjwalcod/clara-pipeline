"""
batch_run.py – Run the full pipeline on all demo + onboarding files.

Expects:
  data/demo/         *.txt  (5 demo transcripts)
  data/onboarding/   *.txt  (5 onboarding transcripts)

Matching is done by filename stem (e.g. acme.txt matches acme.txt).
If no match is found, Pipeline B still runs but will auto-create v1.

Usage:
    python -m scripts.batch_run
    python -m scripts.batch_run --demo-dir data/demo --onboard-dir data/onboarding
    python -m scripts.batch_run --dry-run
"""

import argparse
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from scripts.config     import DEMO_DIR, ONBOARD_DIR, OUTPUT_DIR
from scripts.pipeline_a import run as run_a
from scripts.pipeline_b import run as run_b


SUPPORTED_EXTENSIONS = {".txt", ".md", ".srt", ".vtt"}


def collect_files(directory: Path) -> list[Path]:
    """Return all transcript files from a directory, sorted."""
    files = [
        f for f in sorted(directory.iterdir())
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return files


def match_pairs(demo_files: list[Path], onboard_files: list[Path]) -> list[tuple]:
    """
    Try to match demo files with onboarding files by stem.
    Returns list of (demo_path | None, onboard_path | None) tuples.
    """
    demo_map    = {f.stem.lower(): f for f in demo_files}
    onboard_map = {f.stem.lower(): f for f in onboard_files}

    # Also try matching with common suffix patterns stripped
    def normalise(stem: str) -> str:
        for suffix in ("_demo", "_onboarding", "_onboard", "-demo", "-onboarding"):
            stem = stem.replace(suffix, "")
        return stem

    all_keys = set(normalise(k) for k in demo_map) | set(normalise(k) for k in onboard_map)

    pairs = []
    for key in sorted(all_keys):
        demo_file    = demo_map.get(key) or demo_map.get(f"{key}_demo")
        onboard_file = onboard_map.get(key) or onboard_map.get(f"{key}_onboarding")
        pairs.append((key, demo_file, onboard_file))

    # Handle unmatched files
    for stem, path in demo_map.items():
        norm = normalise(stem)
        if not any(p[0] == norm for p in pairs):
            pairs.append((norm, path, None))

    for stem, path in onboard_map.items():
        norm = normalise(stem)
        if not any(p[0] == norm for p in pairs):
            pairs.append((norm, None, path))

    return pairs


def run_batch(
    demo_dir:    Path = DEMO_DIR,
    onboard_dir: Path = ONBOARD_DIR,
    dry_run:     bool = False,
) -> dict:
    """
    Process all files. Returns a summary report dict.
    """
    demo_files    = collect_files(demo_dir)
    onboard_files = collect_files(onboard_dir)
    pairs         = match_pairs(demo_files, onboard_files)

    print(f"\n{'='*60}")
    print(f"BATCH RUN  │  {len(demo_files)} demo  +  {len(onboard_files)} onboarding files")
    print(f"{'='*60}")

    results = []

    for account_key, demo_path, onboard_path in pairs:
        print(f"\n── Account: {account_key} ──────────────────────────")
        result = {
            "account_key":  account_key,
            "demo_file":    str(demo_path) if demo_path else None,
            "onboard_file": str(onboard_path) if onboard_path else None,
            "pipeline_a":   None,
            "pipeline_b":   None,
        }

        if dry_run:
            print(f"  [dry-run] Would process: demo={demo_path} | onboard={onboard_path}")
            results.append(result)
            continue

        # ── Pipeline A ──────────────────────────────────────────────
        if demo_path:
            try:
                result["pipeline_a"] = run_a(demo_path)
            except Exception as e:
                print(f"  ❌ Pipeline A failed: {e}")
                traceback.print_exc()
                result["pipeline_a"] = {"status": "error", "error": str(e)}
        else:
            print(f"  [skip] No demo file for {account_key}")

        # ── Pipeline B ──────────────────────────────────────────────
        if onboard_path:
            # Use account_id from pipeline A result if available
            account_id = (result["pipeline_a"] or {}).get("account_id")
            try:
                result["pipeline_b"] = run_b(onboard_path, account_id_override=account_id)
            except Exception as e:
                print(f"  ❌ Pipeline B failed: {e}")
                traceback.print_exc()
                result["pipeline_b"] = {"status": "error", "error": str(e)}
        else:
            print(f"  [skip] No onboarding file for {account_key}")

        results.append(result)

    # ── Summary report ───────────────────────────────────────────────
    total    = len(results)
    a_ok     = sum(1 for r in results if (r["pipeline_a"] or {}).get("status") == "success")
    b_ok     = sum(1 for r in results if (r["pipeline_b"] or {}).get("status") == "success")
    a_err    = sum(1 for r in results if (r["pipeline_a"] or {}).get("status") == "error")
    b_err    = sum(1 for r in results if (r["pipeline_b"] or {}).get("status") == "error")

    report = {
        "run_at":          datetime.now(timezone.utc).isoformat(),
        "total_accounts":  total,
        "pipeline_a":      {"success": a_ok, "error": a_err},
        "pipeline_b":      {"success": b_ok, "error": b_err},
        "accounts":        results,
    }

    # Save report
    report_path = OUTPUT_DIR / "batch_report.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))

    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE")
    print(f"  Pipeline A: {a_ok} success / {a_err} error")
    print(f"  Pipeline B: {b_ok} success / {b_err} error")
    print(f"  Report saved → {report_path}")
    print(f"{'='*60}")

    return report


# ── CLI entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch run Clara Pipeline on all files")
    parser.add_argument("--demo-dir",    default=str(DEMO_DIR))
    parser.add_argument("--onboard-dir", default=str(ONBOARD_DIR))
    parser.add_argument("--dry-run",     action="store_true", help="Print plan without running")
    args = parser.parse_args()

    report = run_batch(
        demo_dir    = Path(args.demo_dir),
        onboard_dir = Path(args.onboard_dir),
        dry_run     = args.dry_run,
    )
    failed = report["pipeline_a"]["error"] + report["pipeline_b"]["error"]
    sys.exit(0 if failed == 0 else 1)
