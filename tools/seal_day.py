#!/usr/bin/env python3
"""Seal one UTC day of Ambient Chronomancy events into the public ledger.

Usage:
    seal_day.py                # seals yesterday (UTC)
    seal_day.py 2026-04-22     # seals a specific UTC date

Reads `ambient_events` from chronomancy.db on quantum-dev via SSH.
Writes `daily/YYYY-MM-DD.jsonl` (events + trailing seal line) and appends
an entry to `LEDGER_INDEX.json` linking each day's seal to the previous
via SHA-256 hash chain.

Only ambient_events (the detector-fire record) is written. User responses
and dispatched-ping routing stay private in the live DB — they are not
required for public verification and surfacing them would push the
ledger into NT-axiom territory (per-user evidence visibility).

The tool does git add + commit, but does NOT push automatically. Run
`git -C <repo> push` after inspecting.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parent.parent
DAILY_DIR = REPO / "daily"
INDEX = REPO / "LEDGER_INDEX.json"
GENESIS = "0" * 64

REMOTE_DB = "/home/quantum-dev/chronomancy-deploy/chronomancy-server/bot/chronomancy.db"


def pull_events(date_str: str) -> list[dict]:
    start = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(days=1)
    script = f"""
import sqlite3, json
c = sqlite3.connect({REMOTE_DB!r})
c.row_factory = sqlite3.Row
rows = c.execute(
    "SELECT event_id, timestamp_utc, detector_name, detector_p, p_combined, "
    "window_size_bytes, substrate_id, kp_index, ledger_eligible, ping_eligible, "
    "detector_detail FROM ambient_events "
    "WHERE timestamp_utc >= ? AND timestamp_utc < ? "
    "ORDER BY timestamp_utc ASC",
    ({start.timestamp()}, {end.timestamp()}),
).fetchall()
print(json.dumps([dict(r) for r in rows]))
"""
    res = subprocess.run(
        ["ssh", "quantum-dev", "python3"],
        input=script, capture_output=True, text=True, check=True,
    )
    return json.loads(res.stdout)


def canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_index() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text())
    return {"entries": [], "last_seal_sha256": GENESIS}


def save_index(idx: dict) -> None:
    INDEX.write_text(json.dumps(idx, indent=2) + "\n")


def seal(date_str: str, *, force: bool = False) -> pathlib.Path:
    idx = load_index()
    if any(e["date"] == date_str for e in idx["entries"]) and not force:
        raise SystemExit(f"{date_str} already sealed; pass --force to re-seal")

    events = pull_events(date_str)

    DAILY_DIR.mkdir(exist_ok=True)
    target = DAILY_DIR / f"{date_str}.jsonl"
    event_lines = [canonical(e) for e in events]
    events_blob = "\n".join(event_lines)
    events_sha = sha256_hex(events_blob)

    prev_seal = idx["last_seal_sha256"]
    seal_core = {
        "date": date_str,
        "event_count": len(events),
        "events_sha256": events_sha,
        "prev_seal_sha256": prev_seal,
        "sealed_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    seal_self_hash = sha256_hex(prev_seal + events_sha + canonical(seal_core))
    seal_core["seal_sha256"] = seal_self_hash
    seal_line = canonical({"__seal__": seal_core})

    with target.open("w") as f:
        for ln in event_lines:
            f.write(ln + "\n")
        f.write(seal_line + "\n")

    idx["entries"].append({
        "date": date_str,
        "file": str(target.relative_to(REPO)),
        "event_count": len(events),
        "seal_sha256": seal_self_hash,
    })
    idx["last_seal_sha256"] = seal_self_hash
    save_index(idx)

    print(f"sealed {target.relative_to(REPO)}  events={len(events)}  seal={seal_self_hash[:12]}…")
    return target


def git_commit(date_str: str, event_count: int) -> None:
    msg = f"daily seal {date_str}: {event_count} event{'s' if event_count != 1 else ''}"
    subprocess.run(["git", "-C", str(REPO), "add", "daily/", "LEDGER_INDEX.json"], check=True)
    # Detect whether there's anything staged.
    diff = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--cached", "--quiet"],
    )
    if diff.returncode == 0:
        print("nothing to commit (already clean)")
        return
    subprocess.run(["git", "-C", str(REPO), "commit", "-m", msg], check=True)
    print(f"committed: {msg}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("date", nargs="?", help="YYYY-MM-DD UTC (default: yesterday)")
    ap.add_argument("--no-commit", action="store_true", help="seal only, don't git commit")
    ap.add_argument("--force", action="store_true", help="overwrite existing seal for this date")
    args = ap.parse_args()

    if args.date:
        date_str = args.date
    else:
        yday = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)
        date_str = yday.isoformat()

    seal(date_str, force=args.force)
    if not args.no_commit:
        idx = load_index()
        cnt = next(e["event_count"] for e in idx["entries"] if e["date"] == date_str)
        git_commit(date_str, cnt)


if __name__ == "__main__":
    main()
