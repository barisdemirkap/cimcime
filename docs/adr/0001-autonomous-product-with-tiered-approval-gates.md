---
status: accepted
---

# Cimcime is an autonomous product, not a human-learning curriculum, gated by three approval thresholds

Cimcime performs forward-deployed-engineer work itself — it is not a curriculum that teaches the
user to become an FDE. It acts autonomously using its own logic and analysis for everything except
three explicit approval gates: production-level delivery/deployment, outbound communication to a
real third party, and any action that spends real money or changes external account/billing
settings. Reversible work is protected by version control and backup/snapshots instead of
per-action permission. The standing rule, in the user's words: Cimcime owns "how," the user owns
"why" — execution and analysis are automated, rationale and intent are not.

## Considered options

- A curriculum/coaching system that teaches the human the FDE skillset (rejected — the user wants
  the work done, not to do it themselves).
- Approval required before every non-trivial action (rejected — too slow for genuine autonomy;
  reversibility via VCS/snapshots covers the same risk for anything short of the three gates).
