# chronomancy-ledger

Public ledger for **Ambient Chronomancy** — an architecture for continuous coupling detection, grounded in the Model of Pragmatic Information (von Lucadou, Römer, Walach) and running as a new mode inside the Chronomancy platform.

This repository is the epistemic infrastructure. It holds:

- **Architecture & design docs** — [`docs/VISION.md`](docs/VISION.md), [`docs/AMBIENT.md`](docs/AMBIENT.md), [`docs/AMBIENT_GAMIFICATION.md`](docs/AMBIENT_GAMIFICATION.md), [`docs/MPI_PRIMER.md`](docs/MPI_PRIMER.md)
- **Challenge protocol** — [`docs/CHALLENGE_PROTOCOL.md`](docs/CHALLENGE_PROTOCOL.md), the tamper-evident QRNG trial and bounty rulebook for active Psi Games; [`docs/CHALLENGE_V0_BINARY.md`](docs/CHALLENGE_V0_BINARY.md) freezes the first implementable binary task; [`docs/CHALLENGE_IMPLEMENTATION_MAP.md`](docs/CHALLENGE_IMPLEMENTATION_MAP.md) maps it onto the backend; [`docs/CHALLENGE_V0_BINARY_PREREG_TEMPLATE.md`](docs/CHALLENGE_V0_BINARY_PREREG_TEMPLATE.md) is the freeze template
- **Pre-registrations** — hypotheses locked in *before* the data window they cover, one file per preregistration, committed to git and timestamped by GitHub
- **Daily Merkle-sealed event log** — `daily/YYYY-MM-DD.jsonl` + `LEDGER_INDEX.json`, committed by a cron after each UTC day closes
- **Primary sources** — [`references/`](references/), the papers the architecture cites

The git log is the Merkle chain. Every commit records when something was said, and the content-addressing makes post-hoc rewriting detectable.

## Vision

Chronomancy is a public proof system for extraordinary human
performance: a consumer-scale, cryptographically auditable laboratory
for testing whether human attention, timing, intention, and symbolic
context can show measurable structure against quantum randomness.

The longer thesis lives in [`docs/VISION.md`](docs/VISION.md).

## What Ambient Chronomancy is

A second mode inside Chronomancy, next to the existing standard mode (π-seeded deterministic sync + random pings inside a user window). In ambient mode, the phone is not producing entropy and the user is not clicking. A server-side quantum RNG runs continuously, a detector ensemble watches it, and when the stream does something statistically unusual the user gets a ping:

> *Something just shifted. What do you notice?*

The user responds with the existing Chronomancy primitives — UP / DOWN / tags — or ignores the ping. Response rate is itself data.

See [`docs/AMBIENT.md`](docs/AMBIENT.md) for the six-layer architecture.

## What Chronomancy Challenge is

Chronomancy Challenge is the active-trial counterpart to Ambient
Chronomancy. Users run pre-committed QRNG prediction, influence, timing,
or witnessing experiments; each scored trial is hashed into a Merkle
tree; and a public bounty protocol defines what would count as
extraordinary performance.

The boundary is deliberate: ambient mode rewards witnessing and supports
aggregate science, while active Psi Games may support per-user scoring
because the target statistic is explicit and pre-registered. See
[`docs/CHALLENGE_PROTOCOL.md`](docs/CHALLENGE_PROTOCOL.md) and the first
implementation target,
[`docs/CHALLENGE_V0_BINARY.md`](docs/CHALLENGE_V0_BINARY.md). The backend
mapping lives in
[`docs/CHALLENGE_IMPLEMENTATION_MAP.md`](docs/CHALLENGE_IMPLEMENTATION_MAP.md).
The first pre-registration should be cut from
[`docs/CHALLENGE_V0_BINARY_PREREG_TEMPLATE.md`](docs/CHALLENGE_V0_BINARY_PREREG_TEMPLATE.md)
only when the protocol is ready to freeze.

## What's different from most psi instruments

The two loud commitments in the design are load-bearing:

1. **Non-transmissibility is an engineering constraint, not a rhetorical one.** The NT axiom (Lucadou et al. 2007, p. 56) says entanglement correlations cannot be used to transmit signals. The four operational conditions of a "signal" (ibid. p. 58–59) tell you exactly which product features violate it — per-user anomaly leaderboards, "who is most anomalous" rankings, accumulated per-user evidence scores. Those are structurally excluded. Per-moment p-values attached to historical pings and aggregate statistics across all users are fine. See [`docs/AMBIENT_GAMIFICATION.md`](docs/AMBIENT_GAMIFICATION.md).

2. **The ledger is public before any claim is made about it.** Every hypothesis this instrument tests is committed to `preregistrations/` with a git timestamp before the data window for that hypothesis opens. Every daily event log is SHA-256 sealed and committed. No post-hoc cherry-picking, no garden-of-forking-paths problem.

## Status

```
  phase 0  preconditions                        active
  phase 1  minimum viable ambient                pending
  phase 2  calibration vs verified-null          pending
  phase 3  self-run (author alone)               pending
  phase 4  closed beta                           pending
  phase 5  pre-registered hypotheses             pending
  phase 6  public beta + data accumulation       pending
```

## Layout

```
  docs/
    VISION.md                   moonshot thesis and product framing
    AMBIENT.md                 architecture
    AMBIENT_GAMIFICATION.md    scoring / gamification design, NT-compatible
    CHALLENGE_PROTOCOL.md      active QRNG trial + bounty protocol
    CHALLENGE_V0_BINARY.md     first active binary task specification
    CHALLENGE_IMPLEMENTATION_MAP.md
                                backend migration and route map
    CHALLENGE_V0_BINARY_PREREG_TEMPLATE.md
                                active-track pre-registration template
    MPI_PRIMER.md              theory primer with verbatim source quotes
  
  preregistrations/            pre-registered hypotheses, one per file
                               (none yet — phase 5)
  
  daily/                       daily Merkle-sealed event logs
                               (none yet — phase 1)
  
  references/                  primary-source PDFs cited by the architecture
    lucadou_romer_walach_2007.pdf   NT axiom, four-conditions-of-signal,
                                    decline effect derivation, CMM method
    roemer_synEnd_2010.pdf          extended version of the above
    roemer_20years_gqt.pdf          review, 2013, "Twenty Years of GQT"
    lucadou_causality_entanglement.pdf   workshop paper, causality side
    jse_lucadou.pdf                 Journal of Scientific Exploration
  
  LEDGER_INDEX.json            (empty until first daily seal)
  LICENSE                      Apache-2.0 (docs + code)
```

## References included

The PDFs in `references/` are academic papers in the public record. They are included here for reference by the design docs and are the property of their respective authors and publishers. Original hosting:

- Lucadou, Römer, Walach 2007 — [Tressoldi mirror](http://www.patriziotressoldi.it/cmssimpled/uploads/includes/QuantumLocadou07.pdf)
- Römer 2010 — [author's page](https://hartmannroemer.de/VerallgQTh/SynEnd2010.pdf)
- Römer 2013 — [Journal of Anomalistik](https://www.anomalistik.de/images/pdf/zfa/JAnom23-1_145_Roemer_en.pdf)
- Lucadou causality — [WorkshopPsiTheory 2019](https://workshoppsitheory.wordpress.com/wp-content/uploads/2019/06/lucadou_paper.pdf)
- Lucadou in JSE — [Journal of Scientific Exploration](https://journalofscientificexploration.org/index.php/jse/article/download/3459/2143)

## License

[Apache 2.0](LICENSE) for docs + code. Primary sources in `references/` retain their original copyrights.
