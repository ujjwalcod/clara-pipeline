"""
storage.py – Read and write versioned output artefacts to disk.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from scripts.config import OUTPUT_DIR


def _account_dir(account_id: str, version: str) -> Path:
    d = OUTPUT_DIR / account_id / version
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_memo(account_id: str, memo: dict, version: str = "v1") -> Path:
    path = _account_dir(account_id, version) / "memo.json"
    path.write_text(json.dumps(memo, indent=2))
    print(f"  [storage] Saved memo  → {path.relative_to(OUTPUT_DIR.parent.parent)}")
    return path


def save_agent_spec(account_id: str, spec: dict, version: str = "v1") -> Path:
    path = _account_dir(account_id, version) / "agent_spec.json"
    path.write_text(json.dumps(spec, indent=2))
    print(f"  [storage] Saved spec  → {path.relative_to(OUTPUT_DIR.parent.parent)}")
    return path


def save_changelog(account_id: str, changelog: dict) -> Path:
    path = _account_dir(account_id, "v2") / "changelog.json"
    path.write_text(json.dumps(changelog, indent=2))

    # Also write human-readable markdown
    md_path = _account_dir(account_id, "v2") / "changelog.md"
    md_path.write_text(_changelog_to_md(changelog))
    print(f"  [storage] Saved changelog → {path.relative_to(OUTPUT_DIR.parent.parent)}")
    return path


def load_memo(account_id: str, version: str = "v1") -> dict | None:
    path = OUTPUT_DIR / account_id / version / "memo.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def load_agent_spec(account_id: str, version: str = "v1") -> dict | None:
    path = OUTPUT_DIR / account_id / version / "agent_spec.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def list_accounts() -> list[str]:
    if not OUTPUT_DIR.exists():
        return []
    return [d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()]


def _changelog_to_md(changelog: dict) -> str:
    lines = [
        f"# Changelog – {changelog.get('account_id', '')}",
        f"",
        f"**Updated:** {changelog.get('updated_at', '')}",
        f"**Source:** {changelog.get('source', '')}",
        f"",
        "## Summary",
        changelog.get("summary", ""),
        "",
        "## Changes",
    ]
    for change in changelog.get("changes", []):
        field   = change.get("field", "")
        old_val = change.get("old_value", "—")
        new_val = change.get("new_value", "—")
        reason  = change.get("reason", "")
        lines.append(f"### `{field}`")
        lines.append(f"- **Before:** `{old_val}`")
        lines.append(f"- **After:**  `{new_val}`")
        if reason:
            lines.append(f"- **Reason:** {reason}")
        lines.append("")
    if changelog.get("unresolved_conflicts"):
        lines += ["## Unresolved Conflicts", ""]
        for c in changelog["unresolved_conflicts"]:
            lines.append(f"- {c}")
    return "\n".join(lines)
