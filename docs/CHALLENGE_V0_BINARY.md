# Challenge v0 Binary Protocol

*Implementation specification, draft 0 - 2026-05-01*

---

## Status

`challenge_v0_binary` is the first active Psi Games protocol intended
for backend implementation.

This specification is narrower than
[`CHALLENGE_PROTOCOL.md`](CHALLENGE_PROTOCOL.md). The umbrella protocol
defines the research and bounty boundary. This document defines one
scored game precisely enough for implementation, audit, and later
pre-registration.

No paid bounty should open until this spec has been reviewed, frozen,
and referenced by a pre-registration.

## Summary

The participant predicts a binary target generated from a hardware QRNG.
Each target is committed before the participant input is accepted. Each
completed trial becomes a canonical JSON leaf. Session leaves are folded
into a Merkle root. Session statistics are recomputable from the revealed
trial records.

The null hypothesis is simple:

```text
H0: participant hit probability p = 0.5
```

The default alternative for bounty eligibility is one-sided:

```text
H1: participant hit probability p > 0.5
```

## Roles

```text
participant   user making binary predictions
operator      Chronomancy service operator
verifier      any third party recomputing proofs and statistics
reviewer      independent statistician or review panel for bounty claims
```

## Trial States

```text
committed   target fixed, participant input not yet recorded
answered    participant input recorded, target not yet revealed
revealed    target revealed and outcome computed
void        trial excluded by a pre-registered objective rule
```

A trial may move only forward:

```text
committed -> answered -> revealed
committed -> void
answered  -> void
```

Revealed trials are never voided unless a pre-registered exclusion rule
applies to the whole affected class of trials.

## Target Generation

The target is one bit:

```text
target_bit = qrng_byte & 1
```

The QRNG sample used for target generation must be captured before
participant input.

Initial source:

```text
QWR4U009 - QCC MED1MQ16 1Mbps device
```

Fallback source policy:

- Fallbacks are not allowed for bounty-eligible sessions in v0.
- If QWR4U009 is unavailable, the backend must reject new
  bounty-eligible sessions or mark them as non-bounty practice.
- Practice sessions may use a declared fallback only if the session
  record includes `bounty_eligible: false`.

## Commitment

For each trial, the backend creates a commitment before accepting the
participant input.

The commitment binds:

- the unrevealed target bit;
- the QRNG sample hash;
- the protocol version;
- the session and trial identifiers;
- the sequence number;
- the participant pseudonym;
- the server code version.

Minimum commitment record:

```json
{
  "type": "trial_commitment",
  "protocol_version": "challenge_v0_binary",
  "session_id": "uuid",
  "trial_id": "uuid",
  "sequence_num": 1,
  "participant_hash": "hmac-sha256",
  "qrng_source": "QWR4U009",
  "qrng_sample_hash": "sha256",
  "target_commitment": "sha256",
  "commitment_salt_hash": "sha256",
  "created_at_utc": "2026-05-01T00:00:00.000Z",
  "server_code_version": "git-sha"
}
```

The target commitment is:

```text
target_commitment = sha256(canonical_json({
  "protocol_version": "challenge_v0_binary",
  "trial_id": trial_id,
  "target_bit": target_bit,
  "commitment_salt": random_256_bit_hex
}))
```

The raw `commitment_salt` is private until reveal. The
`commitment_salt_hash` lets the verifier confirm after reveal that the
salt itself was not swapped.

```text
commitment_salt_hash = sha256(commitment_salt)
```

## Participant Input

Valid input:

```text
0
1
```

The backend must reject any other input for scored sessions.

Minimum input record:

```json
{
  "type": "trial_input",
  "trial_id": "uuid",
  "participant_input": 1,
  "answered_at_utc": "2026-05-01T00:00:01.000Z",
  "input_client": "web",
  "input_latency_ms": 1000
}
```

The participant may not edit input after submission.

## Reveal

After input is recorded, the backend reveals:

- target bit;
- commitment salt;
- QRNG sample metadata needed for audit;
- outcome.

Minimum reveal record:

```json
{
  "type": "trial_reveal",
  "trial_id": "uuid",
  "target_bit": 0,
  "commitment_salt": "hex",
  "outcome": "miss",
  "score": 0,
  "revealed_at_utc": "2026-05-01T00:00:02.000Z",
  "scoring_rule": "binary_exact_match_v0"
}
```

Scoring:

```text
score = 1 if participant_input == target_bit else 0
```

## Canonical JSON

All hashes use canonical JSON:

- UTF-8 encoding;
- object keys sorted lexicographically;
- no insignificant whitespace;
- integers encoded as JSON numbers;
- timestamps encoded as ISO-8601 UTC strings with millisecond precision;
- absent optional values omitted rather than encoded as null.

Reference Python form:

```python
json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
```

Reference helper implementation:
[`tools/challenge_v0_binary.py`](../tools/challenge_v0_binary.py).

## Trial Leaf

A revealed trial leaf is the hash of one canonical record:

```json
{
  "type": "challenge_v0_binary_trial",
  "commitment": {},
  "input": {},
  "reveal": {}
}
```

Hash:

```text
leaf_hash = sha256(canonical_json(trial_leaf_record))
```

Void trials are included in the session record but excluded from scored
statistics. Their void reason must be one of the published reason codes.

## Merkle Tree

Leaves are ordered by `sequence_num` ascending.

If the number of leaves at a level is odd, duplicate the final hash at
that level before computing the next level. Parent hashes are:

```text
parent = sha256(left_child_hex + right_child_hex)
```

The session root is the final hash.

For a one-leaf session:

```text
merkle_root = leaf_hash
```

## Session Statistics

Definitions:

```text
n = count(revealed, non-void trials)
h = sum(score)
hit_rate = h / n
expected_hits = n * 0.5
sigma = sqrt(n * 0.5 * 0.5)
z = (h - expected_hits) / sigma
```

The primary p-value for session display is the exact one-sided binomial
tail:

```text
p_value = P[X >= h], where X ~ Binomial(n, 0.5)
```

The z-score is retained because it is easy to reason about over large
claim windows and matches the bounty threshold language. The exact
binomial p-value is authoritative for verification.

Minimum session summary:

```json
{
  "type": "challenge_v0_binary_session",
  "protocol_version": "challenge_v0_binary",
  "session_id": "uuid",
  "participant_hash": "hmac-sha256",
  "bounty_eligible": true,
  "qrng_source": "QWR4U009",
  "trial_count": 1000,
  "void_count": 0,
  "hit_count": 517,
  "hit_rate": 0.517,
  "z_score": 1.075174,
  "p_value_exact_one_sided": 0.141,
  "merkle_root": "sha256",
  "started_at_utc": "2026-05-01T00:00:00.000Z",
  "completed_at_utc": "2026-05-01T00:20:00.000Z",
  "server_code_version": "git-sha"
}
```

## Cumulative Claim Window

A bounty claim is evaluated over a frozen set of sessions.

Claim statistics:

```text
N = sum(n_i)
H = sum(h_i)
Z = (H - N * 0.5) / sqrt(N * 0.25)
P = P[X >= H], where X ~ Binomial(N, 0.5)
```

Draft v0 bounty gate:

```text
minimum N: 100,000 revealed non-void trials
minimum Z: 5.0
primary P: exact one-sided binomial tail
confirmation: required
```

Approximate hit count required at `N = 100,000`:

```text
sigma = sqrt(100000 * 0.25) = 158.113883
required excess hits = ceil(5 * sigma) = 791
required hits = 50,791
required hit rate = 50.791%
```

The threshold can be recomputed with:

```bash
python3 tools/challenge_v0_binary.py threshold --trials 100000 --z 5
```

This is not a final prize promise. It is the draft mathematical gate for
the first binary protocol.

## Claim Opening

The backend may open a claim automatically when:

- `N >= 100000`;
- `Z >= 5.0`;
- all sessions are `bounty_eligible: true`;
- no required Merkle proofs are missing;
- no active fraud review flag exists;
- the participant satisfies account, consent, identity, and jurisdiction
  requirements.

Opening a claim does not authorize payment. It starts verification and
confirmation.

## Confirmation Block

The confirmation block is a fresh pre-registered session set run after
the claim opens.

Draft confirmation requirement:

```text
minimum confirmation N: 20,000
minimum confirmation Z: 3.0
same protocol version: challenge_v0_binary
source: QWR4U009 or an independently declared hardware QRNG
observation: live or enhanced logging required
```

The exact confirmation rule must be frozen before any claimant starts
the block.

## Verification Checklist

A verifier must be able to:

1. recompute every `target_commitment` from revealed target bits and
   salts;
2. recompute every trial `leaf_hash`;
3. recompute every session `merkle_root`;
4. verify inclusion proofs for selected leaves;
5. recompute session `n`, `h`, hit rate, z-score, and exact p-value;
6. recompute claim-window `N`, `H`, `Z`, and exact p-value;
7. confirm all included sessions used `challenge_v0_binary`;
8. confirm all included sessions used eligible QRNG sources;
9. confirm all voided trials use published reason codes;
10. confirm the claim window was frozen before final review.

## Published Void Reason Codes

```text
server_outage
incomplete_reveal
qrng_healthcheck_failed
duplicate_trial_id
malformed_input
scoring_bug_class
automation_detected
replay_detected
protocol_version_mismatch
```

Every void record must include:

```json
{
  "type": "trial_void",
  "trial_id": "uuid",
  "reason_code": "qrng_healthcheck_failed",
  "voided_at_utc": "2026-05-01T00:00:02.000Z",
  "void_policy_version": "challenge_v0_binary_voids"
}
```

## Non-Bounty Practice Sessions

Practice sessions may relax UX limits but must remain clearly labeled.

Practice sessions may:

- use fallback entropy;
- allow shorter trial counts;
- display casual stats;
- omit bounty claim eligibility.

Practice sessions must not:

- be merged into bounty claim windows;
- be marketed as verified extraordinary performance;
- silently upgrade into bounty-eligible sessions after completion.

## Implementation Notes

Backend tables likely need fields for:

- protocol version;
- QRNG source;
- bounty eligibility;
- commitment hash;
- commitment salt encrypted or private until reveal;
- trial leaf hash;
- session Merkle root;
- void reason code;
- server code version;
- claim window ID.

The first API surface should be:

```text
POST /api/training/sessions
POST /api/training/sessions/{session_id}/trials/commit
POST /api/training/trials/{trial_id}/answer
POST /api/training/trials/{trial_id}/reveal
GET  /api/verify/sessions/{session_id}
GET  /api/verify/trials/{trial_id}
POST /api/bounty/claims
```

The implementation can combine commit and answer into one latency-safe
endpoint if the commitment record is created first and returned in the
same response cycle. The audit log must still preserve the ordering.

## Open Items Before Freeze

- Choose whether v0 is prediction language, influence language, or a
  neutral "binary task" in user-facing copy.
- Decide whether target generation uses the low bit of each QRNG byte or
  a bias-corrected bit extraction step.
- Publish a trial-path calibration certificate specific to binary target
  generation.
- Decide whether Solana anchoring is required for v0 claims or only for
  paid public launch.
- Finalize bounty amount and payout currency.
- Obtain legal review of prize terms and eligible jurisdictions.
