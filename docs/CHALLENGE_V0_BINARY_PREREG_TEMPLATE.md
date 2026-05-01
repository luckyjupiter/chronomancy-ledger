# Challenge v0 Binary Pre-registration Template

*Template, draft 0 - 2026-05-01*

---

## Use

Copy this template into `preregistrations/` only when the
`challenge_v0_binary` protocol is ready to freeze.

Do not use a draft copy as an active pre-registration. The active file
must contain concrete dates, commit SHAs, protocol versions, thresholds,
and review rules before any eligible data window opens.

## Header

```text
Title: Chronomancy Challenge v0 Binary Pre-registration
Protocol: challenge_v0_binary
Protocol spec: docs/CHALLENGE_V0_BINARY.md
Reference verifier: tools/challenge_v0_binary.py
Date committed UTC: YYYY-MM-DD
Protocol freeze commit: <git-sha>
Window opens UTC: <timestamp or trigger>
Window closes UTC: <timestamp or trigger>
Status: active
```

## Purpose

This pre-registration defines the first bounty-eligible active trial
window for the Chronomancy binary QRNG challenge.

The document is a rule lock. Any analysis not specified here is
exploratory unless separately pre-registered before the relevant data is
collected.

## Protocol

```text
protocol_version: challenge_v0_binary
task: binary QRNG target prediction
valid participant input: 0 or 1
target generation: target_bit = qrng_byte & 1
primary QRNG source: QWR4U009
fallback sources: none for bounty eligibility
session eligibility: bounty_eligible = true
practice sessions: excluded
```

## Hypotheses

Primary null:

```text
H0: participant hit probability p = 0.5
```

Primary alternative:

```text
H1: participant hit probability p > 0.5
```

## Primary Statistic

The primary statistic is the exact one-sided binomial tail over the
frozen claim window:

```text
N = total revealed non-void bounty-eligible trials
H = total hits
P = P[X >= H], where X ~ Binomial(N, 0.5)
Z = (H - N * 0.5) / sqrt(N * 0.25)
```

The exact binomial p-value is authoritative. Z-score is retained for
threshold language and human readability.

## Bounty Gate

Draft values to freeze:

```text
minimum N: 100,000
minimum Z: 5.0
minimum hits at N=100,000: 50,791
maximum exact one-sided p at threshold: approximately 2.87156e-7
confirmation required: yes
```

The backend may open a claim when all of the following are true:

- `N >= 100000`;
- `Z >= 5.0`;
- every included session is `bounty_eligible = true`;
- every included session uses `protocol_version = challenge_v0_binary`;
- every included session uses an eligible QRNG source;
- every included session has a recomputable Merkle root;
- participant account, consent, identity, and jurisdiction gates pass;
- no active fraud, automation, replay, or protocol-abuse flag exists.

## Confirmation Block

Draft values to freeze:

```text
minimum confirmation N: 20,000
minimum confirmation Z: 3.0
primary statistic: exact one-sided binomial tail
protocol: challenge_v0_binary
QRNG source: QWR4U009 or named independent hardware QRNG
observation: enhanced logging or live observation required
```

The confirmation block starts only after the initial claim window is
frozen. Its sessions must not be selected from earlier data.

## Exclusion Rules

Allowed void reason codes:

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

Voids must be objective. Sessions or trials may not be excluded because
they lower a participant's score.

## Multiple Comparisons

This pre-registration covers only `challenge_v0_binary`.

If additional active protocols are bounty eligible during the same
public challenge period, the bounty gate must specify whether familywise
or false-discovery correction applies across protocols.

Draft v0 position:

```text
No cross-protocol correction is needed if only challenge_v0_binary is
eligible for the first paid bounty window.
```

## Data Lock

Claim window freezes when either:

```text
participant crosses N >= 100,000 and Z >= 5.0
```

or:

```text
the public data window closes without a threshold crossing
```

After freeze:

- session IDs are fixed;
- trial IDs are fixed;
- void records are fixed unless an already-defined class-wide bug is
  discovered;
- statistics are recomputed by the reference verifier;
- confirmation block may be opened if the bounty gate was crossed.

## Verification

The review package must include:

- protocol spec commit SHA;
- this pre-registration commit SHA;
- list of included session IDs;
- session summaries;
- trial-level proof material or public verification endpoint links;
- Merkle roots and anchors;
- exact recomputation output from `tools/challenge_v0_binary.py`;
- fraud and automation review summary;
- confirmation block results, if applicable.

## Result Labels

```text
registered       active data window opened under this file
verified         Merkle proofs and statistics recomputed
claim-opened     initial bounty gate crossed
confirmed        confirmation block passed
paid             bounty disbursed
failed           did not cross the gate
rejected         audit, eligibility, or confirmation failed
```

## Legal And Product Boundary

This pre-registration does not claim that anomalous ability exists. It
defines the conditions under which Chronomancy will treat a result as a
verified challenge result.

Subscription fees buy access to software, experiments, records, and
verification tools. The bounty is a standing research prize funded by
the operating entity or its designated treasury, not a wager among users.
