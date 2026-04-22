# MPI / Generalized Quantum Theory — a primer

Quote-level extract from the primary source so the architecture docs
can be grounded in verifiable language rather than paraphrase.

**Primary source:** von Lucadou, W., Römer, H., Walach, H. (2007).
"Synchronistic Phenomena as Entanglement Correlations in Generalized
Quantum Theory." *Journal of Consciousness Studies* 14(4): 50–74.
PDF: [`references/lucadou_romer_walach_2007.pdf`](../references/lucadou_romer_walach_2007.pdf).

Supplementary texts in [`references/`](../references/): Römer 2010,
Römer 2013 ("Twenty Years of Generalized Quantum Theory"), Lucadou
"Causality and Entanglement" workshop paper, JSE piece.

---

## The claim, in their own words

> *"Synchronistic or psi phenomena are interpreted as entanglement
> correlations in a generalized quantum theory. From the principle that
> entanglement correlations cannot be used for transmitting information,
> we can deduce the decline effect, frequently observed in psi
> experiments, and propose strategies for suppressing it and improving
> the visibility of psi effects."*
> — Abstract, p. 50

## The NT axiom, verbatim

> *"Entanglement correlations cannot be used for transmitting signals
> or controllable causal influences. … Let us call it the NT ('non
> transmission') axiom."*
> — p. 56

This is an **axiom** in Generalized Quantum Theory, not an empirical
claim. It is imported from ordinary quantum theory (where it is
provable — Eberhard 1978) and postulated to hold in the wider GQT
setting.

## What counts as a "signal" — the four conditions

The NT axiom negates the conjunction of these four:

> *"There is a **predefined** pair of quantities, one at the emitter
> side Σ₂ one at the receiver side Σ₁.*
>
> *There is a stable correlation between the registered values of the
> quantities.*
>
> *Controllable manipulations at the emitter side are possible, and
> their effect can be registered at the receiver side.*
>
> *Conclusions on the nature of the manipulations must be possible."*
> — p. 58–59

If all four hold → it's a signal → NT says it cannot exist as a
genuine entanglement correlation.

If any one fails → it's not a signal → NT does not prohibit it.

**The last three are the engineering targets for ambient architecture.**
In particular: "controllable manipulations" at any side means that if
the user can reliably change the RNG's behavior to achieve a desired
outcome, we have crossed into signal territory and NT predicts the
effect will dissolve.

## Three consequences derived from NT (not observed and rationalized — derived)

> *"(a) The well known decline effect: Whenever a psi-experiment at
> first shows positive results, later data or replications will wipe
> out the primarily observed effect and will, possibly after
> tantalising revivals, eventually level off to the null hypothesis."*
>
> *"(b) The reciprocity between effect strength and reliability of psi
> phenomena: the more drastic an effect, the less reproducible it
> turns out to be and vice versa."*
>
> *"(c) Elusiveness (evasion): When one tries to pinpoint psi
> phenomena, they show a tendency to disappear, where they are sought
> for and to surface at some other unexpected place. This is the
> so-called displacement effect."*
> — p. 52–53

These three are **theorems** under NT + organizational closure, not
empirical mysteries. A phenomenon obeying NT must behave this way.

## The upper bound on effect size under strict replication

> *"The effect-size of each psi-experiment should decline with the
> number of trials. … In the simplest case E < const/√n holds if n is
> the number of replication. Only for strict replications const is a
> constant which depends on the experimental setting."*
> — p. 61

This makes the PEAR decline (0.46 → 0.042 → 0.0094 over three
replications, Table 1 p. 64) not a failure of the phenomenon but a
confirmation of the theory.

## Organizational closure — the precondition for the effect

> *"Paranormal or synchronistic phenomena occur in complex systems of
> persons and parts of the physical world, which are strongly coupled
> by many physical, mental and in particular emotional ties. Systems
> of this kind have a property, called organizational closure in
> system theory. Varela formulated the 'Closure Thesis' in the
> following way: 'Every autonomous system is organizationally
> closed'."*
> — p. 57

> *"As stated above, the creation of the organizational closure of the
> psycho-physical system is of paramount importance. Furthermore, one
> has to take care, that it is created mainly by the experimental
> conditions for the subjects and not for the experimenter. Sometimes
> experimenters are more motivated than the subjects and then the data
> are difficult to interpret and lead to so-called experimenter-
> effects."*
> — p. 63

Organizational closure = the psycho-physical system is coherent as a
whole; its state depends on the subject's state; observation of part
of the system perturbs the whole. This is the **precondition** — no
closure means no entanglement means no correlation.

## The CMM strategy — how to detect without creating a signal

> *"In order to reduce the decline effect, one should make positive
> use of the evasion phenomenon. This can be done by simultaneous
> registration of as many different correlations as possible. Psi
> effects will then show up as transitory, jumping unexpected and
> statistically unlikely patterns in the correlation matrix."*
> — p. 60

> *"The null-hypothesis is given by the number of chance-correlations.
> With any replication of the experiment the structure, direction, and
> strength of these correlations may change, but the total number and
> total strength can remain high if the experimental conditions are
> the same. It is impossible to violate the NT axiom because it is not
> known in advance which correlations will show up and with which
> signs."*
> — p. 63

**Operational translation:** the load-bearing statistic is the
**count** of correlations exceeding nominal significance, not the
identity of any specific correlation. Individual correlations evaporate
under replication; the total count persists. This is how Lucadou's
group demonstrated significant effect sizes (Table 2, p. 68; Z-scores
2.25–6.22 across five studies) while keeping each specific correlation
unpredictable.

## The two ways out of the signal trap

> *"(1) The experimental setting is designed in such a way that only
> correlations could be measured, which cannot be (mis-) used for any
> signal-transfer, like in the EPR-case, and,*
>
> *(2) the experimental setting allows the effect to 'displace' in an
> unpredictable way."*
> — p. 61–62

CMM satisfies (1). Ambient mode with a wide correlation space satisfies
(2).

## Conclusion, in their words

> *"We have made an argument that synchronistic, anomalistic or
> PSI-effects are likely due to non-local correlations that can be
> expected according to Generalised Quantum Theory in systems with
> sufficient closure that contain complementary local and global
> features or observables. … This approach explains two pervasive
> features of PSI effects: The elusiveness and the decline of
> experimental results through replication. We have pointed out that
> indirect strategies exist, though, which could be used for
> experimental validation of our claim."*
> — p. 69

---

## How this maps onto Ambient Chronomancy

- **Layer 1 (continuous QRNG)** honors condition (2) — no predefined
  emitter/receiver, no stable correlation to "discover" — the stream
  is just running, and the user's life is the embedding
- **Layer 2 (detector ensemble)** realizes CMM — the count of
  simultaneously-significant detectors is the load-bearing statistic;
  individual detectors may fire or not, the ledger records everything
- **Layer 3 (context binding)** supplies the embedding — the
  organizationally-closed system includes operator, device, time,
  location, geomagnetic field, recent participation history
- **Layer 4 (the ping)** is phenomenological feedback, not a signal
  channel — it invites the operator to witness, not act
- **Layer 5 (personal ledger)** maintains organizational closure by
  coupling the operator's self-model to the recorded stream
- **Layer 6 (Merkle ledger)** is the pre-commitment apparatus that
  makes the CMM count-of-correlations test credible after the fact

## What "violates NT" in product terms

Anything that gives the operator a **controllable manipulation at the
emitter side** whose **predefined effect is registered at the receiver
side**, where the **operator can infer what manipulation produced the
effect**.

In ambient-mode product features, this rules out:

- Per-user leaderboards ranked by anomaly rate (the operator can
  optimize the rate and then knows what they did to produce it)
- Per-user bits-of-evidence scores (same)
- "Your anomaly strength this week" accumulators (same)
- Any coaching that would teach the user how to generate more anomalies

It does **not** rule out:

- Per-moment p-values attached to past pings (historical, not a
  score-to-optimize)
- Global aggregate statistics across all users (no individual can
  manipulate them meaningfully)
- Witnessing-behavior leaderboards (rewards showing up, not producing)
- Pre-registered aggregate hypothesis tests (Sidereal, Kp, etc.)
- Personal ledgers that show "pings you responded to", "tags you used",
  "streak" (all reward presence, not production)

This is the distinction [AMBIENT_GAMIFICATION.md](AMBIENT_GAMIFICATION.md)
operationalizes.
