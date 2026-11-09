---
status: accepted
---

# A CI workflow mirrors `main` to the public `cimcime` repo, because interactive pushes are blocked

Publishing to the public repo (`barisdemirkap/cimcime`, branch `master`) used to depend on an
interactive Claude session running `git push`, which Claude Code's auto-mode classifier blocks
(allow rules do not override it). That left the user running commands by hand, repeatedly.

`.github/workflows/publish-cimcime.yml` now runs on the self-hosted runner after every push to
`main` and pushes `HEAD` to `cimcime` `master` with the repo secret `CIMCIME_PUSH_TOKEN`.

- The push is fast-forward only, never forced: if the public repo has diverged the job fails
  loudly instead of overwriting anything.
- `actions/checkout` runs with `persist-credentials: false`, otherwise its `GITHUB_TOKEN`
  credentials take precedence over the PAT and the push is rejected (the first run failed this way).
- The token is a fine-grained PAT scoped to `barisdemirkap/cimcime` with Contents read/write,
  valid for one year. Renew it before it expires, or publishing stops. The failure is visible
  as a red `publish-cimcime` run, not silent.
- This does not replace ADR-0001: pushing to `main` is routine; anything that goes public for the
  first time or changes what is public in a significant way still goes through the user.

## Verifying a publish

A green run is not enough on its own. Compare heads:
`gh api repos/barisdemirkap/cimcime/commits/master --jq .sha` must equal `git rev-parse HEAD`.
