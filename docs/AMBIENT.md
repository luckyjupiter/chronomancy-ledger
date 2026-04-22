# Ambient Chronomancy

An architecture for continuous coupling detection

*Design note, draft 1 — 2026-04-22*

---

## The shift

The active-trial paradigm — operator pays attention, picks a moment, clicks a button, gets a bit — assumes the phenomenon lives in the decision. Under Decision Augmentation Theory (May, Utts, Spottiswoode 1994) this is coherent: the operator's precognitive sensitivity selects favorable moments from the random stream, and the click is the channel. Under that reading, without a decision point there is no measurement.

But the Model of Pragmatic Information (von Lucadou, Römer, Walach) tells a different story. The coupling is not in the click; it is in the *embedding* of the random process in a meaningful context. The correlation arises because the RNG is situated inside a larger system — operator, body, environment, intention, day — that carries pragmatic information. Meaning is the substrate; the click is only one way of sampling it.

If MPI is closer to right than DAT, continuous background monitoring is not merely possible. It may be the architecturally correct form of the instrument, and active trials may be a narrow special case that pays for statistical legibility with a loss of phenomenological range.

This is the hypothesis Ambient Chronomancy is built to test and, if it holds, to deploy.

## Theoretical posture

Nothing in this document assumes the phenomenon is settled. The empirical record across psi-RNG instruments shows small, persistent, Bonferroni-surviving aggregate bias together with elevated rare-event frequencies — findings consistent with both a weak continuous coupling and a non-stationary process where hot windows punctuate flat baseline. The long-run mean regresses to chance, as non-transmissibility would predict; the tails do not behave like the tails of a stationary random process.

The architecture below takes that empirical shape at face value and asks: what instrument best captures it? Not *what does it mean*. Not *what can we harness from it*. Just: what shape of device does the shape of the phenomenon call for?

The answer proposed here is a six-layer stack that treats the random stream as a temporal annotator — marking moments rather than transmitting content — and surfaces those markings to a user whose ongoing life is the embedding context.

## Architecture

### Layer 1 — Continuous QRNG stream

A server-side hardware quantum random number generator runs continuously on the Chronomancy backend, producing raw bits into a rolling buffer. The substrate of record for this deployment is a **QCC MED1MQ16 1Mbps device (serial QWR4U009)**, plugged into the Chronomancy server and dedicated to ambient mode. The device is one of Scott Wilber's ComScire-lineage entropy sources; it is not shared with QTrainer (which uses a separate PQ128MS at QWR70158).

Target throughput is ~1 Mbit/s raw, conditioned via the existing ComScire pipeline into whitened bytes. Layer 1 does not generate bits on demand in response to a user action. It is ambient. The operator is not performing; the operator is living, and the device is along for the ride.

(Alternative substrates — `/dev/hwrng`, an ANU-style network QRNG, or an additional 1MHz MED — can be added as secondary channels once the primary pipeline is calibrated. The correlation-matrix detection method (Lucadou's CMM) naturally extends to multi-channel data.)

### Layer 2 — Anomaly detection

Continuous signal processing watches the stream for departures from expected random behavior. The specific detectors matter less than breadth of coverage:

- Runs tests (Wald–Wolfowitz) for sequential dependence
- Chi-square deviations from the uniform byte distribution
- Spectral anomalies at physiologically and environmentally relevant frequencies (resonance band, Schumann harmonics, circadian)
- Correlation-matrix structure when additional channels are available
- Persistent-homology summaries on trajectory windows if the compute budget allows

No single detector is expected to dominate. Detector p-values are combined via Fisher's method (or Cauchy combination if detector independence fails calibration), and a single combined p-value per window drives the anomaly event.

Thresholds must be set such that false-positive rate under a verified-stationary control stream matches the nominal chance rate — this is the falsification precondition for the entire architecture.

This design directly realizes Lucadou's Correlation Matrix Method: *"Psi effects will then show up as transitory, jumping unexpected and statistically unlikely patterns in the correlation matrix. … The null-hypothesis is given by the number of chance-correlations."* (Lucadou, Römer, Walach 2007, p. 60 and p. 63.) The load-bearing statistic is the count of simultaneously-significant detectors, not the identity of any single one — because individual correlations evaporate under replication while the count persists, and the NT axiom is not violated because no specific manipulation-to-outcome channel is exposed.

### Layer 3 — Context binding

When an anomaly fires, the system captures whatever contextual data it has permission to access at that moment:

- Timestamp (UTC and local sidereal, derived from user timezone)
- Geomagnetic index (Kp, NOAA API, cached with 3h refresh)
- Time since the user's last Chronomancy ping (standard or ambient)
- Whether the user has recently participated in /sounding
- Coarse-grained location (user-controlled; Country / UTC offset resolution by default)
- Device state at ping dispatch time (minimal — whether Telegram session is active)

This is the embedding layer. It is what lets the aggregate analysis (Layer 6) test whether anomalies cluster around identifiable external variables, and it is what lets the personal analysis (Layer 5) surface whether anomalies cluster around identifiable life patterns.

Content of the user's actual experience at the moment is *not* captured automatically. It is captured only through the user's response to the ping (Layer 4), and only at whatever resolution the user chooses to provide.

### Layer 4 — The ping

When an anomaly clears threshold, the user gets a notification via the existing Chronomancy Telegram bot. The language is the existing Chronomancy register:

> Something just shifted. What do you notice?

The user responds with the existing Chronomancy primitives — UP, DOWN, tags, optional photo or text — or ignores the ping. Response rate itself is data.

The ping is not claiming the anomaly *means* anything. It is not an oracle. It is a marker: the random stream, embedded in your life, just did something non-random. You are the only person who can tell whether that corresponds to anything in your present moment. Tell us what you noticed, or don't.

### Layer 5 — The personal ledger

Anomaly events plus user responses accumulate into a personal timeline. Over weeks, the user can see:

- Whether pings land on moments that feel significant (self-reported)
- Whether pings cluster around particular times, states, or contexts
- Whether the pings they marked "high signal" share structural features with each other
- Which tags they use most often

This is phenomenological utility in the Randonautica sense. The random process is pointing at moments in the user's life. The user, over time, develops calibration — learns what their own marked moments look like. The app is not telling them what the moments mean. It is giving them a structured surface on which meaning can be noticed.

### Layer 6 — The aggregate ledger

Across all users, anomaly events form a global stream. Timestamps, detector signatures, and non-personally-identifying context features are Merkle-sealed to a public ledger on a rolling basis. The ledger is this repository's `daily/` directory. Each daily JSONL file is hashed, the hash is recorded in `LEDGER_INDEX.json`, and the whole thing is committed to git. **The git log is the Merkle chain.** GitHub's commit timestamps anchor it externally. No blockchain required.

Once the ledger is sealed for a given window, no one — not the user, not the operator of the service, not a later researcher — can alter which anomalies were flagged, when, or under what context without the tampering being detectable. This is the infrastructure von Lucadou's Correlation Matrix Method gestures at but never had.

With a sealed ledger, the science becomes tractable:

- Do anomaly rates correlate with geomagnetic indices?
- Do they correlate with sidereal time in the way May and Spottiswoode found for anomalous cognition?
- Do they cluster around collective attention events (breaking news, shared cultural moments, eclipses)?
- Do user-rated "high signal" pings have distinguishable signatures at the stream level from low-signal pings?
- Do paired users (opt-in, both running ambient mode) show cross-correlated anomaly timing that exceeds shuffled-pair baseline?

None of these require anyone to believe the phenomenon is real. They only require that the data be captured honestly and analyzed against pre-registered hypotheses. Pre-registrations commit to `preregistrations/` with a git timestamp *before* the data window they cover opens. The ledger does the epistemic work.

## What this architecture is not

It is not an oracle. It does not answer questions. It does not produce content. It does not claim to transmit information.

It is not a productivity tool. It does not tell the user what to do with marked moments.

It is not a search engine for the unknown. The ambient stream is not being queried; it is being witnessed.

It is not a commercial promise of hit rates, accuracy percentages, or operational capability. The only promise is: the instrument will mark moments in a way that is either above-chance or not, the data will be published honestly, and the user will be invited to notice.

These negative specifications are load-bearing. Every failure mode in the adjacent commercial field has come from overclaiming on one of these axes. The architecture is designed to make overclaiming structurally difficult — the ledger is public, the scoring is grounded in bits of evidence against pre-registered nulls, the user experience is phenomenological rather than informational. See [AMBIENT_GAMIFICATION.md](AMBIENT_GAMIFICATION.md) for the specific product-surface commitments this entails.

## Relationship to the existing Chronomancy stack

Chronomancy today ships two kinds of pings through its Telegram bot and mini-app:

- **Random window pings** — scheduled inside a per-user window set by `/window`, fired at unpredictable times within that window.
- **π-seeded global sync pings** — the `GlobalSyncResponse` mechanism in `miniapp/server.py`, using `PI_SEED = 3.14159265358979323846` as the deterministic seed for calculating the next shared sync moment. The time is known to the protocol but not announced to users in advance.

Both of these are **standard mode**. They operate without reference to the QRNG stream — the randomness is in the scheduling, not in a quantum substrate.

Ambient mode sits beside them, not on top of them:

| Component | Standard mode | Ambient mode |
|---|---|---|
| When the ping fires | random time within window, or π-sync | when Layer 2 detectors cross threshold |
| What triggers it | scheduler | continuous QRNG + anomaly detection |
| Entropy substrate | none (scheduled) or π (deterministic) | hardware QRNG (QWR4U009 1MHz MED) |
| Data captured | ping_responses UP/DOWN + tags | ping_responses UP/DOWN + tags, keyed to an anomaly event |
| Per-user scoring | existing vibes / streak logic | witnessing metrics only (see GAMIFICATION.md) |
| Public ledger | none | daily Merkle-sealed JSONL |

Per-user window configuration gets a mode toggle: `[standard (π + random) | ambient (anomaly)]`. At most one is active per user at a time. A user can switch modes between windows; they cannot run both in parallel (to avoid double-pinging and to keep the research comparison between modes clean).

Nothing about standard mode changes. Ambient mode adds new handlers, a new collector service, and the public ledger.

## Open questions

1. **Detector calibration.** False-positive rate under verified-stationary control must match the nominal chance rate before any of the positive analysis means anything. This is not optional and it should happen before any user sees an ambient ping. The calibration run is itself committed to the ledger as evidence.
2. **Ping fatigue.** If anomalies fire too often, the ping loses phenomenological weight and the user stops responding. If too rarely, the ledger accumulates slowly and aggregate analysis takes years to reach power. Target rate per user per day needs prototyping with real operators. The design intent is 1–3 pings per user per day, rate-limited even when the underlying detector fires more often; the ledger still records every anomaly regardless of which users were pinged.
3. **Thermal/throughput budget.** The MED1MQ16 produces 1 Mbit/s raw; the detector ensemble at 60s windows runs at a few percent CPU. Non-issue on the Chronomancy server.
4. **The DAT vs. MPI question becomes testable.** Standard mode is the DAT instrument (operator selects a moment via response or non-response to a scheduled ping). Ambient mode is the MPI instrument (the stream selects the moment; the operator witnesses). If ambient anomalies correlate with user-marked significance at rates comparable to standard-mode hits, MPI is winning. If ambient produces chance-level correlation while standard mode produces above-chance, DAT is winning. This platform, running both modes with honest pre-registration, is the cleanest experimental test of the distinction the field has had.
5. **Non-transmissibility as engineering constraint.** If the NT axiom is real, any product feature that tries to extract actionable content from ambient anomalies will cause the effect to dissolve. See [AMBIENT_GAMIFICATION.md](AMBIENT_GAMIFICATION.md) for the proposed resolution — grounded in the four-condition definition of "signal" from Lucadou, Römer & Walach (2007), p. 58–59.
6. **Scott Wilber's new work.** Recent QCC papers argue that scalar-drift frameworks regress to the mean and that richer representations are needed. Topological data analysis on trajectory windows is the obvious candidate and can be implemented as a Layer 2 detector with existing tooling. Running parallel to Scott rather than coordinated lets the public ledger be the comparison.

## What to prototype first

If this document is useful, the order of operations is:

1. Claim QWR4U009 for Chronomancy via a systemd unit (`chronomancy-qrng@QWR4U009.service`) and stream bytes to a socket / mmap buffer distinct from the QTrainer pipeline.
2. Write `ambient_collector.py` with the three-detector ensemble and Fisher combiner; run it against `secrets.token_bytes()` piped into the same pipeline for 72h. Verify empirical FPR matches nominal at both 0.01 and 0.001 thresholds. Commit the calibration run as a sealed daily log.
3. Add `ambient_events`, `ambient_pings`, `ambient_responses` tables to the Chronomancy DB.
4. Extend the Telegram bot with `/ambient` commands (opt-in, status, pause, witness leaderboard, science link).
5. Run ambient mode on the author alone for 2–4 weeks with no other user base. Phenomenological sanity check.
6. Pre-register the first aggregate hypotheses (sidereal time, Kp correlation, paired cross-correlation) in `preregistrations/` before inviting beta users.
7. Small closed beta. Measure response rate, ping fatigue, retention.
8. Publish pre-registrations and open to public beta. Let the data accumulate.

Steps 1–4 are a few days of work. Steps 5 and onward are time-gated on real humans and real operator-weeks of data.

---

## Primary sources

The theoretical framing in this document rests on these texts; the PDFs are in [`../references/`](../references/) and direct quotations with verifiable page numbers are in [`MPI_PRIMER.md`](MPI_PRIMER.md).

- von Lucadou, W., Römer, H., Walach, H. (2007). "Synchronistic Phenomena as Entanglement Correlations in Generalized Quantum Theory." *Journal of Consciousness Studies* 14(4): 50–74.
- Römer, H. (2010). Extended version of the above, manuscript on the author's site.
- Römer, H. (2013). "Twenty Years of Generalized Quantum Theory." *Zeitschrift für Anomalistik*.
- May, E., Utts, J., Spottiswoode, S.J.P. (1994). "Decision Augmentation Theory: Towards a Model of Anomalous Mental Phenomena." CIA STARGATE archive document CIA-RDP96-00789R003200210001-3.
- Atmanspacher, H., Römer, H., Walach, H. (2002). "Weak Quantum Theory: Complementarity and Entanglement in Physics and Beyond." *Foundations of Physics* 32: 379–406.

---

*This is a design note, not a specification. The theoretical framing is contested paradigm; the architectural proposal is one way of honoring the empirical shape of the phenomenon without overclaiming mechanism or utility. The document exists to be argued with.*
