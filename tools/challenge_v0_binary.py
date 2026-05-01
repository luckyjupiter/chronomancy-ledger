#!/usr/bin/env python3
"""Reference helpers for the Chronomancy challenge_v0_binary protocol.

This is intentionally small and dependency-free. It exists so the docs,
backend, and independent verifiers can agree on canonical JSON, SHA-256
hashing, Merkle root construction, z-scores, and exact binomial tails.

Usage:
    python3 tools/challenge_v0_binary.py threshold --trials 100000 --z 5
    python3 tools/challenge_v0_binary.py session path/to/session.json

The session JSON shape expected by the CLI is:

{
  "trials": [
    {
      "commitment": {...},
      "input": {"participant_input": 1},
      "reveal": {"target_bit": 1, "score": 1}
    }
  ]
}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def canonical_json(obj: Any) -> str:
    """Return the protocol canonical JSON representation."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def trial_leaf_hash(trial: dict[str, Any]) -> str:
    record = {
        "type": "challenge_v0_binary_trial",
        "commitment": trial["commitment"],
        "input": trial["input"],
        "reveal": trial["reveal"],
    }
    return sha256_hex(canonical_json(record))


def target_commitment(protocol_version: str, trial_id: str, target_bit: int, commitment_salt: str) -> str:
    payload = {
        "protocol_version": protocol_version,
        "trial_id": trial_id,
        "target_bit": target_bit,
        "commitment_salt": commitment_salt,
    }
    return sha256_hex(canonical_json(payload))


def verify_trial(trial: dict[str, Any]) -> list[str]:
    """Return a list of verification errors for one revealed trial."""
    errors: list[str] = []
    commitment = trial["commitment"]
    input_record = trial["input"]
    reveal = trial["reveal"]

    protocol_version = commitment["protocol_version"]
    trial_id = commitment["trial_id"]
    target_bit = int(reveal["target_bit"])
    commitment_salt = reveal["commitment_salt"]

    expected_salt_hash = sha256_hex(commitment_salt)
    if commitment.get("commitment_salt_hash") != expected_salt_hash:
        errors.append("commitment_salt_hash mismatch")

    expected_target_commitment = target_commitment(
        protocol_version=protocol_version,
        trial_id=trial_id,
        target_bit=target_bit,
        commitment_salt=commitment_salt,
    )
    if commitment.get("target_commitment") != expected_target_commitment:
        errors.append("target_commitment mismatch")

    participant_input = int(input_record["participant_input"])
    expected_score = 1 if participant_input == target_bit else 0
    if int(reveal["score"]) != expected_score:
        errors.append("score mismatch")

    expected_outcome = "hit" if expected_score else "miss"
    if reveal.get("outcome") != expected_outcome:
        errors.append("outcome mismatch")

    return errors


def merkle_root(leaf_hashes: list[str]) -> str:
    if not leaf_hashes:
        raise ValueError("cannot compute Merkle root for empty session")

    level = leaf_hashes[:]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [
            sha256_hex(level[i] + level[i + 1])
            for i in range(0, len(level), 2)
        ]
    return level[0]


def z_score(hit_count: int, trial_count: int) -> float:
    if trial_count <= 0:
        raise ValueError("trial_count must be positive")
    return (hit_count - trial_count * 0.5) / math.sqrt(trial_count * 0.25)


def required_hits_for_z(trial_count: int, z: float) -> int:
    if trial_count <= 0:
        raise ValueError("trial_count must be positive")
    return math.ceil(trial_count * 0.5 + z * math.sqrt(trial_count * 0.25))


def binomial_tail_one_sided(hit_count: int, trial_count: int) -> float:
    """Return P[X >= hit_count] for X ~ Binomial(trial_count, 0.5).

    Uses a log-sum-exp tail calculation, stable for the 100k-trial bounty
    threshold without scipy.
    """
    if not 0 <= hit_count <= trial_count:
        raise ValueError("hit_count must satisfy 0 <= hit_count <= trial_count")

    log_half = math.log(0.5)
    terms = [
        math.lgamma(trial_count + 1)
        - math.lgamma(k + 1)
        - math.lgamma(trial_count - k + 1)
        + trial_count * log_half
        for k in range(hit_count, trial_count + 1)
    ]
    m = max(terms)
    return math.exp(m + math.log(sum(math.exp(t - m) for t in terms)))


def summarize_session(session: dict[str, Any]) -> dict[str, Any]:
    trials = session["trials"]
    verification_errors = {
        str(t["commitment"].get("trial_id", i)): errors
        for i, t in enumerate(trials)
        if (errors := verify_trial(t))
    }
    leaf_hashes = [trial_leaf_hash(t) for t in trials]
    hit_count = sum(int(t["reveal"]["score"]) for t in trials)
    trial_count = len(trials)
    return {
        "trial_count": trial_count,
        "hit_count": hit_count,
        "hit_rate": hit_count / trial_count if trial_count else None,
        "z_score": z_score(hit_count, trial_count),
        "p_value_exact_one_sided": binomial_tail_one_sided(hit_count, trial_count),
        "merkle_root": merkle_root(leaf_hashes),
        "leaf_hashes": leaf_hashes,
        "verification_errors": verification_errors,
        "verified": not verification_errors,
    }


def cmd_threshold(args: argparse.Namespace) -> None:
    hits = required_hits_for_z(args.trials, args.z)
    summary = {
        "trial_count": args.trials,
        "z_threshold": args.z,
        "required_hits": hits,
        "required_hit_rate": hits / args.trials,
        "exact_one_sided_p": binomial_tail_one_sided(hits, args.trials),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


def cmd_session(args: argparse.Namespace) -> None:
    session = json.loads(Path(args.path).read_text())
    summary = summarize_session(session)
    if not args.include_leaves:
        summary.pop("leaf_hashes", None)
    print(json.dumps(summary, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    threshold = sub.add_parser("threshold", help="compute hits required for a z threshold")
    threshold.add_argument("--trials", type=int, required=True)
    threshold.add_argument("--z", type=float, required=True)
    threshold.set_defaults(func=cmd_threshold)

    session = sub.add_parser("session", help="summarize and verify a session JSON file")
    session.add_argument("path")
    session.add_argument("--include-leaves", action="store_true")
    session.set_defaults(func=cmd_session)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
