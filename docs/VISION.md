# Chronomancy Vision

*Draft 0 - 2026-05-01*

---

## One Sentence

Chronomancy is a public proof system for extraordinary human performance:
a consumer-scale, cryptographically auditable laboratory for testing
whether human attention, timing, intention, and symbolic context can
show measurable structure against quantum randomness.

## The Question

Chronomancy is built around one hard question:

> Can humans demonstrate measurable, repeatable performance against
> quantum randomness under conditions strict enough that skeptics have to
> take the result seriously?

Most projects in this domain ask for belief. Chronomancy asks for proof.

It does not begin by claiming that anomalous cognition exists. It begins
by building the machine that would make such a claim worth hearing.

## The Problem

There is no credible proving ground for people who claim unusual
intuition, precognition, timing sensitivity, or influence over random
systems.

Existing options fail in predictable ways:

- private claims cannot be audited;
- laboratory studies are small, slow, and reputationally radioactive;
- consumer apps optimize engagement instead of evidence;
- skeptics are usually right to distrust unsealed data;
- believers often get stories but not protocols;
- institutions avoid the field because bad claims have poisoned the
  category.

The result is a dead zone. If someone has a real anomalous ability,
there is nowhere serious to demonstrate it. If nobody does, there is no
large, clean, public null result to close the question.

Chronomancy fills that gap.

## The Core Idea

Chronomancy turns anomalous-performance claims into auditable software
objects.

Every serious trial has:

- a protocol version;
- a QRNG source;
- a target commitment before user input;
- a participant input;
- a reveal;
- a score;
- a canonical trial hash;
- a Merkle session root;
- a verification path;
- a pre-registered interpretation rule.

The platform does not ask anyone to trust the operator. It gives
participants, skeptics, researchers, and funders enough public structure
to recompute the claim themselves.

The slogan is:

> If someone can do the impossible, Chronomancy should make it
> undeniable. If nobody can, Chronomancy should make the null result
> useful.

## What It Is Not

Chronomancy is not a psychic-power promise.

It is not a casino, prediction market, or user-funded jackpot.

It is not an oracle. It does not tell users what to do. It does not
promise that quantum randomness carries messages.

It is not a vibes product with scientific decoration.

It is instrumentation first: a high-integrity experimental network with
a consumer interface.

## The Product

The user-facing product begins as a set of simple experiments:

- binary QRNG prediction;
- directional influence;
- sequence prediction;
- timing selection;
- ambient witnessing;
- paired-user sessions;
- symbolic/glyph tagging.

Users subscribe for access to tools, training modes, personal records,
verification links, and research participation. The subscription buys
the software service. It is not a wager.

The bounty is a separate standing research prize. It pays only when a
participant clears public statistical gates, passes audit, and replicates
in a confirmation phase.

## The Wedge

The first wedge is intentionally boring:

```text
Predict one bit.
Commit the target before input.
Reveal the target after input.
Score hit or miss.
Hash the trial.
Fold trials into a Merkle root.
Recompute the p-value.
```

A bit is either `0` or `1`. A user is either right or wrong. The null
model is simple. The verifier is small. The result can be explained to a
skeptic in one minute.

This is the credibility wedge. Once the simple protocol is trusted, the
system can expand into richer and stranger protocols without losing its
epistemic spine.

## The Two Research Surfaces

Chronomancy has two surfaces that should remain distinct.

### Active Challenge

Active Challenge is where bounty-eligible scoring belongs.

Participants intentionally make predictions or attempt influence tasks
against pre-committed QRNG targets. Scores can accumulate because the
statistic is explicit, the protocol is public, and the target was fixed
before the action.

The first protocol is
[`challenge_v0_binary`](CHALLENGE_V0_BINARY.md).

### Ambient Chronomancy

Ambient Chronomancy is passive witnessing.

A hardware QRNG runs continuously. Detector ensembles mark statistically
unusual windows. Users may receive pings and report what they notice.
This surface is for aggregate science and phenomenology, not per-user
anomaly production.

Ambient mode rewards witnessing: response rate, days active, tag
richness, and historical per-moment p-values. It does not rank users by
anomaly rate.

This distinction is important. Active Challenge can test explicit
performance. Ambient Chronomancy can map the context in which anomalies,
reports, symbols, and collective events cluster.

## Why It Is Defensible

Chronomancy is defensible because it refuses to overclaim.

The platform can say:

- we test anomalous performance against quantum randomness;
- the QRNG target is committed before the user acts;
- the scoring rule is known before the session starts;
- trial records are tamper-evident;
- session statistics are independently recomputable;
- major claims require pre-registration;
- bounties require audit and confirmation;
- null results are still published and useful.

The platform should not say:

- users will unlock powers;
- precognition is guaranteed;
- subscription payments are entries into a prize pool;
- exploratory results prove anything;
- testimonials are typical without evidence.

The stronger claim is not "believe us." It is:

> Here is the protocol. Here is the data. Here is the proof path. Here is
> the exact statistic. Recompute it.

## Why It Is Innovative

Chronomancy combines pieces that usually live in separate worlds:

- hardware QRNG instrumentation;
- pre-registered experimental design;
- Merkle-verifiable trial records;
- consumer training loops;
- standing research bounties;
- public null results;
- symbolic and contextual self-report;
- aggregate analysis of timing, attention, and environment.

The innovation is not just testing whether users can guess bits. The
innovation is building a trust layer for an entire class of taboo
experiments.

If the field is full of bad claims, the answer is not to ignore it
forever. The answer is to build infrastructure where bad claims die
quickly and real anomalies, if they exist, survive.

## The Dataset

Over time, Chronomancy becomes a new kind of dataset:

- QRNG outputs;
- target commitments;
- user predictions;
- response timing;
- hit/miss histories;
- detector anomalies;
- ambient pings;
- UP/DOWN reports;
- glyphs and tags;
- coarse context;
- sidereal and geomagnetic variables;
- paired-user timing;
- collective attention windows.

The dataset matters even if nobody wins a bounty.

A null result at scale would be valuable. A weak signal would be
valuable. A non-stationary signal would be valuable. A strong,
replicable outlier would be historic.

## The Bounty

The bounty is not the business model. It is the forcing function.

Anyone can claim extraordinary ability. Chronomancy makes the claim
evidentially expensive.

To win, a participant must clear a public gate:

- enough trials;
- enough statistical lift;
- clean commitments;
- clean Merkle proofs;
- no protocol violations;
- no automation or replay;
- independent recomputation;
- confirmation under stricter conditions.

The first draft gate for binary prediction is:

```text
100,000 revealed non-void trials
z >= 5.0
exact one-sided binomial p-value as the authoritative statistic
confirmation required
```

At 100,000 trials, this requires approximately 50,791 hits, or a 50.791%
hit rate. That is small enough to be imaginable and hard enough to be
serious.

## The 1517 Frame

For a moonshot audience, Chronomancy should be framed as sci-fi science
infrastructure.

The pitch is not:

> We built an occult app.

The pitch is:

> We are building the first consumer-scale proof system for extraordinary
> human performance. It combines hardware quantum randomness,
> pre-registered experimental protocols, Merkle-verifiable trials, public
> bounty challenges, and a growing dataset of human attention under
> uncertainty.

Institutions avoid this domain because it is reputationally dangerous.
That is exactly why better infrastructure matters. If the claims are
false, Chronomancy can falsify them cleanly. If there is a real effect,
Chronomancy gives it a path out of anecdote and into public evidence.

## The Category

Chronomancy is ability discovery infrastructure.

It is adjacent to:

- Kaggle for anomalous cognition;
- Strava for intuition training;
- XPRIZE for human-QRNG performance;
- OpenAI-style evals for extraordinary human ability;
- a public observatory for synchronicity, attention, and randomness.

The goal is not to make one game. The goal is to define a new category:
consumer-scale experimental infrastructure for the edges of human
performance.

## The Moonshot

The upside is asymmetric.

If nothing happens, Chronomancy creates the largest high-integrity public
null dataset in a field that badly needs one.

If something small happens, Chronomancy can map it: who, when, under
what protocol, under what context, with what decay, displacement, or
replication behavior.

If something large happens, Chronomancy becomes the discovery layer for a
new domain of human capability.

The moonshot is:

> Either we falsify a century of extraordinary claims with better
> tooling, or we find the first statistically defensible signal of
> extraordinary cognition at consumer scale.

Both outcomes matter.

## Near-Term Roadmap

1. Publish the vision and protocol docs in the public ledger.
2. Freeze `challenge_v0_binary`.
3. Mirror the reference verifier into the backend.
4. Add pre-trial commitments and Merkle roots to active training.
5. Add public verification endpoints.
6. Run private practice sessions marked non-bounty.
7. Publish a QRNG trial-path calibration certificate.
8. Cut the first real pre-registration from the template.
9. Open a tiny closed beta.
10. Only then announce a paid public bounty.

## Closing Thesis

Chronomancy monetizes clarity, not ambiguity.

It gives believers a fair proving ground, skeptics an audit trail,
researchers a dataset, and outliers a shot at demonstrating something
that would otherwise stay trapped in anecdote.

The product is a game on the surface. Underneath, it is a measurement
layer for the weirdest frontier in human performance.
