# Ambient Chronomancy — Gamification & Scoring Design

*Design note, draft 1 — 2026-04-22*

Companion to [AMBIENT.md](AMBIENT.md). Resolves open question 5 (non-transmissibility as engineering constraint) by specifying which product features are compatible with the NT axiom and which are not.

---

## The constraint, stated in one paragraph

The NT axiom (Lucadou, Römer, Walach 2007, p. 56) says that entanglement correlations cannot be used to transmit signals. A "signal" in their formal sense (p. 58–59) requires **all four** of the following:

1. A predefined pair of quantities — one emitter, one receiver.
2. A stable correlation between them.
3. Controllable manipulations at the emitter side whose effect is registered at the receiver side.
4. The receiver can infer the nature of the emitter-side manipulation.

If all four hold, NT predicts the correlation dissolves. The engineering task for ambient-mode product features is: **ensure at least one of the four fails for every user-facing score.** This document specifies which scoring variables satisfy that constraint and which violate it.

## The distinction

```
  REWARDS WITNESSING                          REWARDS PRODUCTION
  (operator's relationship to the stream)     (the stream's deviation from null)
  ────────────────────────                    ──────────────────────────────
  
  days running ambient mode                   per-user anomaly rate
  response rate to pings                      "most anomalous user this week"
  tag diversity / context richness            cumulative bits of evidence per user
  paired-session count                        p-value leaderboard
  witnessing streak length                    per-user hit rate
  ping-attended vs ignored ratio              "anomaly strength" score
  time-to-first-response                      operator-specific effect size
```

The left column is safe because condition (3) fails — the operator cannot controllably manipulate "days running ambient mode" in a way that propagates through the NT axiom; they just show up. And condition (4) fails because even if they could, the aggregate statistics don't decode back to "what the operator did."

The right column violates condition (3) and (4). If you tell an operator "your anomaly rate this week is 1.3σ," you've given them a feedback channel from their own cognitive/attentional state to a numerical score they can optimize. NT predicts the score will decouple from the underlying phenomenon within weeks as soon as the operator starts optimizing against it.

This is not aesthetic caution. It is the theory. Every prior product in this space has failed at exactly this point.

## Scope of p-value display

There is an honest middle path that exposes the quantitative shape of the phenomenon without creating the forbidden feedback channel:

```
  SCOPE                       SAFE?    WHY
  ─────                       ─────    ───
  
  per-moment p-value          YES      attached to a specific past event;
  (attached to a historical            by the time the operator sees it,
  ping, read-only)                     there's no manipulation they can
                                       perform that would alter it
  
  global aggregate stats      YES      no single operator can meaningfully
  (all users, pre-registered           steer a population-level statistic;
  hypothesis tests)                    NT condition (3) fails — there's
                                       no controllable manipulation
                                       at any single emitter side
  
  per-user cumulative         NO       the operator's ongoing behavior can
  evidence                             change the score; they can infer
                                       what behavior produced high scores;
                                       all four NT conditions hold
  
  per-user per-period         NO       same as above, narrower window
  rate
  
  user-vs-user ranking        NO       creates a tournament structure
                                       where the ranking is itself the
                                       emitter-side observable; operators
                                       optimize position, NT dissolves
                                       the effect
```

## Telegram bot commands

```
  /chronomancy           (existing) standard mode — random window pings
                         + π-seeded global sync
  
  /ambient               (NEW) opt into ambient mode. When user sets their
                         /window, they get a mode toggle:
                           [standard (π + random)  |  ambient (anomaly)]
                         At most one mode active per user at a time.
  
  /ambient status        PERSONAL LEDGER — safe metrics only:
                           • days in ambient mode (witnessing streak)
                           • pings this week, response rate %
                           • most-used tags
                           • last 10 pings with per-moment p-value +
                             your response (historical, not a score)
  
  /ambient pause         stop receiving; keeps history
  
  /ambient witness       WITNESSING LEADERBOARD (NOT anomaly leaderboard):
                           top response rates
                           longest witnessing streaks
                           paired-session counts
                         Handles shown only for users who opt in. Top 20.
                         NO per-user anomaly rankings.
  
  /ambient science       link to the public dashboard with:
                           current pre-registered test results
                           aggregate cumulative stats
                           most recent daily seal hash + date
                           explanation of why per-user scores are not shown
                         (the public dashboard is served from
                         chronomancy-ledger, not from the Chronomancy
                         server — keeps the science data public-by-default
                         and separate from private user data)
```

## In-app first-run explainer

When a user first toggles their window into ambient mode, the bot shows this copy (or an equivalent on the mini-app):

> *Ambient mode watches a quantum-random stream in the background. When the stream does something statistically unusual, you'll get a ping.*
>
> *I am not telling you what the shift means. I am not claiming it carries a message. I am saying: this moment was flagged by the detector. You are the only one who can tell whether anything in your present moment corresponds.*
>
> *You'll see your witnessing streak, your response rate, and the per-moment p-value of each past ping. You will not see a leaderboard of "who is most anomalous." This is a deliberate design choice grounded in the theory this instrument is built to test — if individual users could be ranked by anomaly production, the thing we're measuring would disappear under that ranking. So we don't do it.*
>
> *Aggregate statistics across all users are published to a public ledger. If there's a signal to find, it will be in the population data, not in anyone's individual score. Use /ambient science to see the current aggregate numbers and the pre-registered hypotheses they're testing.*

This paragraph is the product's own theoretical commitment, visible at opt-in.

## What the public ledger shows

```
  SHOWS                                         DOESN'T SHOW
  ─────                                         ────────────
  
  total ambient events in window                any user's personal hit rate
  distribution of detector magnitudes           any user's cumulative bits
  sidereal-time distribution of events          per-user rankings
  Kp-index correlation (Spearman)               user-specific anomaly counts
  response-rate × detector-magnitude            which users "score highest"
    relationship (pooled, anonymized)
  paired-pair cross-correlation vs
    shuffled-pair null
  raw event log with hashed user ids
    (pseudonymized, rotating monthly)
  SHA-256 daily seals, git commit history
  pre-registered hypothesis status
    (open / tested / result)
```

The public ledger answers aggregate questions. It does not expose per-user data that would create an optimization target.

## Relationship to Chronomancy's existing standard mode

Ambient mode is a **parallel second mode**, not a replacement. Standard mode (π-seeded global sync + random window pings) is unchanged. It lives inside the existing DAT-shaped paradigm — the user's UP/DOWN response to a scheduled moment is the channel, and the user's vibes / streak / response history is an appropriate score because the decision itself is what's being measured.

Ambient mode is the MPI-shaped parallel. The stream selects the moment; the user witnesses. No per-user decision is the channel; therefore no per-user score is appropriate.

Users can move between modes window-to-window. The cross-mode comparison — same user's behavior in standard vs ambient — is itself data, and is part of what the pre-registered hypotheses will test.

| | Standard mode | Ambient mode |
|---|---|---|
| Theoretical frame | DAT (May, Utts, Spottiswoode 1994) | MPI (Lucadou, Römer, Walach 2007) |
| Channel | the operator's selective response to a scheduled moment | the embedding of the stream in the operator's life |
| Appropriate per-user scoring | vibes / streak / response rate (existing) | witnessing metrics only |
| Public ledger | not required | required |

## What to collect for the aggregate ledger

Per ambient event:

```
  event_id              UUID
  timestamp_utc         exact
  sidereal_local        derived from lat/lng + utc
  detector_signature    which detectors fired at what p
  p_combined            Fisher / Cauchy combination across detectors
  kp_index              latest NOAA value (cached, 3h refresh)
  substrate_id          which QRNG source (QWR4U009 for the initial deploy)
  user_hash             irreversible hash of user_id, rotated monthly
  response_code         UP / DOWN / TAG_* / IGNORED / TOO_LATE
  response_latency_ms   time from dispatch to response
  response_tags         tag strings only (no free text)
```

Not collected: user's actual location, free-text response, any PII beyond the user_hash. The user_hash is irreversible (HMAC with a server-side key), rotated monthly so operators can be tracked within a month (paired-user cross-correlation) but not across months (no persistent anomaly-production dossier).

## Daily seal procedure

```
  each day at 00:05 UTC:
    1. close yesterday's event log (append-only JSONL)
    2. compute SHA-256 of the file
    3. append { date: "YYYY-MM-DD", sha256: "..." } to LEDGER_INDEX.json
    4. git commit to this repo (chronomancy-ledger)
    5. git push; GitHub records the commit timestamp
    6. tag the commit with the date
    7. the git log IS the Merkle chain;
       tampering requires rewriting all subsequent days
```

No blockchain required. GitHub's git log is cryptographically anchored and trivially auditable. If the project scales enough to require independent third-party timestamping, IPFS, Aptos, or an OpenTimestamps proof can be added as a secondary witness, but none is needed for the initial epistemic commitment.

## Pre-registration format

Before any public beta opens, commit a file under `preregistrations/` in this repo:

```
  # Ambient Chronomancy Pre-registration v1
  # Committed YYYY-MM-DD, sealed at [SHA of first post-commit daily seal]
  
  ## Hypotheses to be tested on first 100 days of ambient data:
  
  H1. Anomaly rate will show non-uniform distribution over local
      sidereal time, with a peak within ±2 hours of 13:47 LST
      (Spottiswoode 1997 claim).
      Test: Rayleigh test of uniformity on circular distribution.
      Pre-registered α = 0.05.
  
  H2. Anomaly rate will show positive correlation with the daily
      Kp geomagnetic index.
      Test: Spearman rank correlation over daily aggregate.
      Pre-registered α = 0.05, one-sided.
  
  H3. User-flagged "high significance" responses (UP / tag "felt right")
      will be associated with higher detector magnitudes than ignored
      pings or "DOWN" responses.
      Test: Mann-Whitney U on p_combined distribution split by
      response code.
      Pre-registered α = 0.05, two-sided.
  
  H4. Paired users (opt-in, both running ambient, with explicit
      declared pairing) will show cross-correlated anomaly timing
      exceeding shuffled-pair baseline.
      Test: bootstrap 10,000 shuffled pairs as null; observed
      pair-timing coincidence count percentile.
      Pre-registered α = 0.05, one-sided.
  
  Family-wise Bonferroni: α_per_test = 0.0125 for family significance.
  
  Analysis locked to first 100 days of ambient data OR first 10,000
  events, whichever first. Results committed to ledger within 30 days
  of data window close.
```

The pre-registration is signed (git commit), timestamped (git + GitHub), and sealed (SHA chain). Any subsequent analysis that doesn't match what's pre-registered is either an extension (labeled as such) or misconduct.

## Summary

The NT axiom is not a nuisance to work around. It is the load-bearing constraint that makes the whole architecture honest. The gamification design follows from it:

- Witnessing metrics reward presence, not production — safe.
- Per-moment p-values are historical annotations, not live optimization targets — safe.
- Global aggregates are about the phenomenon, not any operator — safe.
- Per-user anomaly rankings would create the very signal channel NT forbids — structurally excluded.

If the phenomenon the instrument is designed to test is real, this is the only way to measure it that doesn't destroy it. If the phenomenon isn't real, these choices cost nothing and the Merkle ledger will honestly say so.

Either way, the product promises what it can deliver: the instrument will mark moments, the data will be published honestly, the user is invited to notice. No more, no less.
