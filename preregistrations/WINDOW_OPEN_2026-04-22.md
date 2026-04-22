# Ambient Chronomancy — Data Window Open

**Date (UTC):** 2026-04-22
**First dispatched ping (UTC):** 2026-04-22T16:05:58.637Z
**Triggering event:** `c6985089-09bf-4224-9d4e-e45f88646387`

## Detector state at the moment of fire

| quantity | value |
|---|---|
| combined p-value (Fisher) | **7.097 × 10⁻⁴** |
| detector magnitude `−log₁₀(p_combined)` | **3.15** |
| runs test (Wald–Wolfowitz) | p = 5.90 × 10⁻³ |
| χ² byte-frequency | p = 1.82 × 10⁻³ |
| block-frequency (100 blocks) | p = 8.21 × 10⁻¹ |
| window size | 500 000 bytes (4 Mbits) |
| substrate | QWR4U009 (MED1MQ16, 1 Mbps) |

Two of the three independent detectors crossed into the tail
simultaneously; Fisher combination put the resulting p below the
0.001 ping threshold specified in
[`preregistrations/PREREG_2026-04-22_v1.md`](PREREG_2026-04-22_v1.md)
and calibrated against a verified-stationary null in
[`calibration/2026-04-22_ensemble_v1.md`](../calibration/2026-04-22_ensemble_v1.md).

## What this commit does

Per `PREREG_2026-04-22_v1.md` §"Data window and locking":

> **Window opens:** on the first dispatched ping after this
> pre-registration commit lands. Timestamp will be recorded as the
> commit time of the first `daily/` ledger entry following this file.

This file is that record. The 100-day / 10 000-event / 200-responded
countdown for H3 and H4 begins at the timestamp above. Analysis will
run within 30 days of window close, per the pre-registration, and
results will be committed to `results/` with a backlink to
`PREREG_2026-04-22_v1.md`.

## First response

2026-04-22T16:06:03.246Z — direction **DOWN**, ~5 seconds post-delivery.
User was in `ambient_mode = 2` (both, blinded) and had predicted the
ping would be scheduled, not ambient. The blind held.

This is H3 data point 1: `(magnitude = 3.15, response = DOWN)`.

## Governance

This commit's SHA and GitHub timestamp are together the epistemic
commitment for when the data window opened. Any dispute about window
timing — including post-hoc re-litigation of whether a given event
falls inside or outside the window — must be resolved against this
commit and the corresponding `daily/2026-04-22.jsonl` seal that will
be written at UTC 00:15 on 2026-04-23.
