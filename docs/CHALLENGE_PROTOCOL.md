# Chronomancy Challenge Protocol v0

*Design note, draft 0 — 2026-05-01*

---

## Purpose

Chronomancy Challenge is a public, cryptographically auditable protocol
for testing anomalous performance against quantum randomness.

The protocol has three jobs:

1. give participants a serious instrument for prediction, influence,
   timing, and witnessing experiments;
2. make every scored result tamper-evident before it can become a claim;
3. define standing bounty criteria for extraordinary performance under
   pre-registered statistical rules.

This document is not a claim that anomalous ability exists. It is the
rulebook for finding out honestly. A successful claimant earns a bounty
only by satisfying public thresholds under verifiable conditions. A null
result is still useful: it becomes part of the public evidence base.

## Product Boundary

Chronomancy has two research surfaces that must remain distinct.

### Ambient Ledger

Ambient Chronomancy is passive witnessing. A server-side QRNG runs
continuously, detector ensembles mark unusual windows, and users may be
pinged to report what they notice.

Ambient mode is governed by:

- [`AMBIENT.md`](AMBIENT.md)
- [`AMBIENT_GAMIFICATION.md`](AMBIENT_GAMIFICATION.md)
- [`MPI_PRIMER.md`](MPI_PRIMER.md)

Ambient mode does not support per-user anomaly bounties, per-user
anomaly leaderboards, or "most anomalous user" rankings. Its user-facing
metrics reward witnessing: response rate, days active, tag richness,
and historical per-moment p-values. Aggregate analysis belongs in the
public ledger.

### Psi Games

Psi Games are active trials. A participant intentionally makes a
prediction, selects a target, attempts an influence task, or performs a
defined timing task against a QRNG-backed protocol.

Psi Games may support per-user scoring because the target statistic is
explicit, the trial lifecycle is pre-committed, and bounty eligibility
is judged by public rules rather than ambient anomaly production.

The first implementation target is
[`challenge_v0_binary`](CHALLENGE_V0_BINARY.md), a binary QRNG task with
pre-trial target commitments, exact binomial scoring, Merkle session
roots, and a draft 5-sigma bounty gate.

### Bounty Program

The bounty program is a standing research prize. It pays only when a
participant demonstrates performance that clears the published protocol,
survives audit, and replicates in a confirmation phase.

The bounty is not a wager, jackpot, user-to-user market, investment
pool, or promise that participants will develop abilities. Subscription
fees buy access to software, experiments, personal records, and
verification tools. The bounty treasury is funded by the operating
entity, grants, donations, sponsorships, or allocated operating revenue.

## Claims Language

Allowed product language:

- "test anomalous performance against quantum randomness"
- "train with pre-committed QRNG trials"
- "verify every session with a Merkle proof"
- "participate in an open research challenge"
- "earn a bounty if you satisfy the public protocol"
- "experimental; no result is guaranteed"

Disallowed product language:

- "unlock psychic powers"
- "guaranteed precognition"
- "prove you are superhuman" without qualification
- "beat chance and win money" as the primary framing
- "subscriptions go into the prize pool"
- any testimonial implying typical extraordinary results without
  evidence of typicality

The safe thesis is:

> Chronomancy is a Merkle-sealed research game for testing anomalous
> performance against quantum randomness. Members get tools, records,
> and experiments; anyone who beats the public protocol under independent
> verification earns the bounty; all results, including failures,
> strengthen the public signal ledger.

## Trial Lifecycle

Every scored trial follows the same lifecycle.

### 1. Protocol Selection

The participant chooses a published protocol version:

- binary prediction
- directional influence
- sequence prediction
- timing selection
- freestyle witnessing, unscored for bounty eligibility

Each protocol defines its null model, scoring rule, minimum sample size,
and eligible input format before the session starts.

### 2. Commitment

Before the participant sees the target, the system creates a commitment
record containing enough information to prove the target was fixed before
the reveal.

Minimum commitment fields:

```json
{
  "protocol_version": "challenge_v0_binary",
  "session_id": "uuid",
  "trial_id": "uuid",
  "sequence_num": 1,
  "participant_hash": "hmac-rotating",
  "qrng_source": "QWR4U009",
  "qrng_sample_hash": "sha256",
  "target_commitment": "sha256",
  "created_at_utc": "timestamp",
  "server_code_version": "git-sha"
}
```

The commitment is append-only. Once a commitment exists, the target
cannot be changed without detection.

### 3. Participant Input

The participant submits the defined input:

- binary prediction: 0 or 1
- directional influence: UP or DOWN
- sequence prediction: fixed-length symbol sequence
- timing selection: action timestamp within a defined window

The input is timestamped and bound to the commitment.

### 4. Reveal

The system reveals the QRNG-backed target and computes the outcome
according to the protocol's scoring rule.

Minimum reveal fields:

```json
{
  "trial_id": "uuid",
  "participant_input": "0",
  "target_value": "1",
  "outcome": "miss",
  "scoring_rule": "binary_exact_match",
  "revealed_at_utc": "timestamp"
}
```

### 5. Leaf Hash

The commitment, input, reveal, and scoring fields are canonicalized and
hashed into a trial leaf.

```text
leaf_hash = sha256(canonical_json(commitment + input + reveal + score))
```

### 6. Session Root

At session close, all trial leaves are assembled into a Merkle tree. The
session root is stored with session statistics and, when available,
anchored to an external timestamping surface.

Minimum session fields:

```json
{
  "session_id": "uuid",
  "protocol_version": "challenge_v0_binary",
  "participant_hash": "hmac-rotating",
  "trial_count": 1000,
  "hit_count": 517,
  "hit_rate": 0.517,
  "z_score": 1.075,
  "p_value": 0.141,
  "merkle_root": "sha256",
  "started_at_utc": "timestamp",
  "completed_at_utc": "timestamp"
}
```

### 7. Public Verification

A verification endpoint must let any third party confirm:

- the trial leaf is included in the session root;
- the session root is included in the published anchor;
- the scoring rule matches the protocol version;
- the statistics recompute from the revealed trial data.

## QRNG Requirements

The production QRNG source must be a hardware entropy source or a
declared fallback source. Each source receives a stable identifier and a
calibration certificate.

Initial production source:

```text
QWR4U009 — QCC MED1MQ16 1Mbps device
```

Calibration requirements:

- record device identifier and host;
- publish detector or trial-path calibration against a verified null;
- record code version used for calibration;
- define acceptable false-positive or bias bounds before live use;
- seal calibration results in this repository.

Fallback sources are allowed only if the protocol version declares them
before the session starts. Mixed-source sessions are not bounty-eligible
unless the bounty rules explicitly allow that mixture.

## Bounty Eligibility

The default bounty track is binary prediction or binary influence because
the null model is simple and auditable.

Draft v0 threshold:

```text
minimum trials: 100,000
primary threshold: cumulative z >= 5.0
family threshold: adjusted for all eligible protocol tracks
confirmation: required
```

The exact threshold must be frozen in a pre-registration before any paid
public bounty track opens.

Eligibility requirements:

- participant account in good standing;
- completed consent and identity requirements for prize payout;
- trials conducted through approved interfaces;
- no botting, automation, replay, device tampering, multi-accounting, or
  protocol abuse;
- complete Merkle-verifiable trial history;
- no excluded sessions in the claimed trial set unless exclusion rules
  were pre-registered before those sessions began.

## Confirmation Phase

Crossing the threshold opens a claim. It does not automatically pay.

The confirmation phase should include:

1. freezing the claim window and claimed session IDs;
2. independent recomputation of all statistics;
3. verification of Merkle paths and anchors;
4. review of logs for automation, replay, and protocol abuse;
5. a fresh pre-registered replication block under heightened scrutiny;
6. final review by an independent statistician or review panel.

The confirmation block may be live-observed, rate-limited, and run on a
fresh QRNG channel. Its scoring rule and required effect size must be
published before it begins.

## Exclusions And Anti-Gaming

Exclusion rules must be objective and published before the relevant
trial window starts.

Allowed exclusion categories:

- server outage or incomplete reveal;
- QRNG source unavailable or failed health check;
- duplicate trial ID;
- malformed participant input;
- known software bug affecting scoring;
- verified automation or replay;
- protocol version mismatch.

Disallowed exclusion categories:

- removing sessions because they hurt a participant's score;
- changing the claimed window after seeing results;
- changing scoring rules after session close;
- removing outliers without a pre-registered rule.

## Ledger Architecture

Chronomancy uses two related ledger surfaces.

### Research Ledger

This repository seals ambient events, calibration certificates,
pre-registrations, aggregate results, and protocol documents. The git log
is the public hash chain.

### Trial Ledger

The application backend stores trial leaves, session roots, proofs, and
anchors for active Psi Games.

The trial ledger may anchor to:

- this repository;
- OpenTimestamps;
- IPFS;
- Solana;
- another public timestamping surface.

The implementation may evolve, but the verification requirement is
stable: a third party must be able to recompute the result from the
public proof material.

## Privacy Boundary

Public verification should not require doxxing participants.

Public records may include:

- rotating participant hash;
- protocol version;
- trial IDs;
- commitments;
- revealed targets after session close;
- participant inputs when needed for scoring;
- outcomes;
- session statistics;
- Merkle proofs and anchors.

Private records may include:

- legal identity for prize payout;
- payment details;
- IP and device metadata for fraud review;
- free-text notes;
- precise location;
- contact information.

If a participant claims a bounty, the claim terms may require additional
identity disclosure to the operator, the review panel, payment providers,
or tax authorities. Public identity disclosure should be opt-in unless
required by law or by the published prize terms.

## Results Classification

Results must be labeled clearly.

```text
exploratory      not pre-registered; hypothesis-generating only
registered       protocol locked before data collection
verified         Merkle proof and scoring recomputed
claim-opened     threshold crossed; confirmation pending
confirmed        independent review and confirmation passed
paid             bounty disbursed
rejected         claim failed audit or confirmation
```

No marketing copy may describe an exploratory result as proof.

## Implementation Order

1. Publish this protocol document and link it from the ledger README.
2. Freeze [`challenge_v0_binary`](CHALLENGE_V0_BINARY.md) with exact
   scoring math and threshold.
3. Implement pre-trial commitments in Chronomancy Market.
4. Produce Merkle roots for each completed session.
5. Add public session verification.
6. Add bounty claim creation when a participant crosses the threshold.
7. Add independent review and confirmation workflows.
8. Open the first paid bounty only after legal review of prize terms,
   subscription language, and jurisdiction rules.

## Open Questions

- Should the first bounty track test prediction, influence, or both?
- Should confirmation require the same QRNG device or an independent
  device?
- Should Solana anchoring be mandatory at v0, or should git and
  OpenTimestamps be enough for the pilot?
- What minimum fraud signals are required before a claim can be paid?
- What jurisdictions are excluded from bounty eligibility?
- Who sits on the first independent review panel?

---

This protocol is intentionally conservative. The point is not to make an
extraordinary claim sound marketable. The point is to define the machine
that could make such a claim worth taking seriously.
