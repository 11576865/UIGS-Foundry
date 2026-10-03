# Observation: Numerical domain samplers should pin exact semantic endpoints

Date: 2026-10-04
Status: Observation
Scope: numerical UI models / rate-distortion frontier / floating-point boundaries

## Observation

A logarithmically spaced rate-distortion sampling function reconstructed every sample through `exp(log(...))`, including the endpoints. The mathematically exact lower bound of 150000 could therefore become a floating-point value infinitesimally below 150000 and violate the executable-domain predicate.

## Pattern

When minimum and maximum values are semantic boundaries rather than merely approximate samples, construct the interior points numerically but return the exact supplied `min` and `max` at the first and final indices.

Separately, inverse budget transforms should only be tested as invertible inside their feasible domain. A target whose audio/reserve overhead already exceeds the entire budget can legitimately map to a negative residual video bitrate; it is an impossible budget, not an invertible positive-video point.

## Reusable implication

Tests and UI model code should distinguish:
- exact contract boundaries;
- floating interior interpolation;
- infeasible regions.

Do not let floating reconstruction move a contract endpoint across its own admissibility predicate.

Do not promote to Canonical from this single observation.
