# Chronomancy Market Implementation Map

*Planning note, draft 0 - 2026-05-01*

---

## Purpose

This maps the public challenge protocol onto the live
`chronomancy-market` backend without editing that backend directly.

The implementation target is:

- umbrella protocol: [`CHALLENGE_PROTOCOL.md`](CHALLENGE_PROTOCOL.md)
- first scored game: [`CHALLENGE_V0_BINARY.md`](CHALLENGE_V0_BINARY.md)
- reference math/proofs: [`tools/challenge_v0_binary.py`](../tools/challenge_v0_binary.py)

## Current Backend Shape

The live backend already has the right conceptual tables:

```text
training_sessions
trials
user_stats
bounty_config
bounty_claims
merkle_anchors
research_participants
consent_forms
consent_signatures
```

The current `Trial` shape is sufficient for a casual QRNG game but not
for a defensible bounty:

```text
id
session_id
sequence_num
qrng_output
user_input
outcome
timestamp
leaf_hash
```

The challenge protocol needs a two-phase commitment/reveal audit trail,
QRNG source identity, protocol versioning, exact scoring metadata, and
void handling.

## Minimum Model Changes

### TrainingSession

Add:

```text
protocol_version           string, indexed
participant_hash           string
bounty_eligible            boolean, default false
qrng_source                string
void_count                 integer, default 0
hit_count                  integer, default 0
p_value_exact_one_sided    float
server_code_version        string
anchor_id                  nullable FK -> merkle_anchors.id
claim_window_id            nullable UUID/string
```

Keep:

```text
trial_count_target
trials_completed
merkle_root
z_score
hit_rate
status
started_at
completed_at
```

### Trial

Add:

```text
protocol_version           string, indexed
state                      enum/string: committed, answered, revealed, void
participant_hash           string
qrng_source                string
qrng_sample_hash           string
target_commitment          string
commitment_salt_hash       string
commitment_salt            encrypted/private until reveal
target_bit                 nullable integer
commitment_record          JSONB
input_record               JSONB
reveal_record              JSONB
void_record                nullable JSONB
void_reason_code           nullable string
answered_at                nullable timestamptz
revealed_at                nullable timestamptz
server_code_version        string
```

Keep or alias:

```text
qrng_output                legacy/current target storage
user_input
outcome
leaf_hash
timestamp
```

### BountyConfig

Add:

```text
protocol_version
confirmation_min_trials
confirmation_threshold_z
requires_confirmation
terms_version
active_from
active_until
jurisdiction_policy
```

### BountyClaim

Add:

```text
protocol_version
claim_window_id
trial_count
hit_count
hit_rate
p_value_exact_one_sided
merkle_roots              JSONB/list
review_notes              nullable text
confirmation_session_ids  JSONB/list
opened_at
verified_at
rejected_at
paid_at
```

Existing `session_ids`, `cumulative_z`, and `status` remain useful.

## Minimum Services

### `engine/challenge_binary.py`

Responsibilities:

- canonical JSON
- SHA-256 helpers
- target commitment construction
- trial leaf hash construction
- Merkle root construction
- exact one-sided binomial p-value
- z-score and required-hit calculation
- session summary recomputation
- trial verification

This should be copied or adapted from
[`tools/challenge_v0_binary.py`](../tools/challenge_v0_binary.py) so the
backend and public verifier do not diverge.

### `engine/qrng_service.py`

Responsibilities:

- read one or more bytes from QWR4U009;
- expose source id and health status;
- return QRNG sample plus `qrng_sample_hash`;
- reject bounty-eligible sessions when source health is not acceptable;
- make fallback use explicit and mark sessions `bounty_eligible: false`.

### `engine/training_service.py`

Responsibilities:

- start sessions;
- create commitments;
- accept participant input;
- reveal targets;
- close sessions;
- recompute session stats;
- update user stats;
- persist leaf hashes and Merkle roots.

### `engine/bounty_service.py`

Responsibilities:

- detect threshold crossing;
- freeze claim window;
- recompute claim stats;
- create `BountyClaim`;
- enforce account, consent, identity, and jurisdiction gates;
- manage confirmation block status.

## Minimum Routes

```text
POST /api/training/sessions
POST /api/training/sessions/{session_id}/trials/commit
POST /api/training/trials/{trial_id}/answer
POST /api/training/trials/{trial_id}/reveal
POST /api/training/sessions/{session_id}/complete

GET  /api/verify/sessions/{session_id}
GET  /api/verify/trials/{trial_id}
GET  /api/verify/claims/{claim_id}

GET  /api/bounty
POST /api/bounty/claims
GET  /api/bounty/claims/{claim_id}
```

For UX latency, `commit` and `answer` can be combined by an endpoint that
creates the commitment first, returns it, accepts the input, and then
reveals. The database must still preserve the logical ordering.

## Migration Order

1. Add nullable protocol/audit columns to `training_sessions` and
   `trials`.
2. Backfill existing rows as `protocol_version = 'legacy_training'` and
   `bounty_eligible = false`.
3. Add bounty/claim metadata columns.
4. Add indexes for `protocol_version`, `participant_hash`, `state`, and
   `claim_window_id`.
5. Deploy backend code that can read legacy and v0 rows.
6. Only after read compatibility is verified, expose v0 routes.

No existing training history should be silently upgraded into v0 bounty
eligibility.

## Verification Response Shape

`GET /api/verify/sessions/{session_id}` should return:

```json
{
  "protocol_version": "challenge_v0_binary",
  "session": {},
  "trials": [],
  "leaf_hashes": [],
  "merkle_root": "sha256",
  "stats": {
    "trial_count": 1000,
    "hit_count": 517,
    "hit_rate": 0.517,
    "z_score": 1.075174,
    "p_value_exact_one_sided": 0.141
  },
  "verification": {
    "verified": true,
    "errors": {}
  },
  "anchor": {
    "type": "none|git|opentimestamps|solana",
    "reference": null
  }
}
```

The public verifier should be able to feed this response into the
reference helper and recompute the same root and statistics.

## Initial Test Plan

Unit tests:

- canonical JSON key ordering is stable;
- target commitments recompute after reveal;
- score mismatches are caught;
- salt mismatches are caught;
- Merkle roots are stable for odd and even leaf counts;
- exact p-value for 50,791 / 100,000 is about `2.87156e-7`;
- legacy sessions are never bounty eligible.

Integration tests:

- start a v0 session;
- commit one trial;
- answer one trial;
- reveal one trial;
- complete session;
- verify session endpoint returns recomputable stats;
- claim creation refuses under-threshold users;
- claim creation opens for synthetic threshold-crossing data.

## Deployment Guardrails

- Do not restart live services until migrations and route tests pass on a
  copy of the database.
- Do not expose bounty language in the UI until legal terms and
  jurisdiction gates exist.
- Do not enable Solana payment or payout language as part of the
  protocol implementation.
- Keep practice sessions and bounty-eligible sessions visually and
  technically distinct.
- Treat all current QRNG/training data as legacy unless it was generated
  under this protocol after the freeze commit.
