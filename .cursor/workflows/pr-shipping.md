# Workflow: Ship a PR

**When:** Code change ready for review on GitHub (`autorope/donkeycar` or a fork).
**Result:** Focused PR with clear test plan; docs PR noted if needed.

## Steps

1. Branch from `main`; keep scope to one fix/feature.
2. Follow `CONTRIBUTING.md`: pep-8, tests, broad usefulness for new features.
3. Run tests (`.cursor/workflows/run-tests.md`).
4. Open PR against `main` with:
   - What changed (user-facing first)
   - How to test (steps a human can follow; video link if hardware)
   - Link related Issue / donkeydocs PR if any
5. Respond to review comments; do not leave the PR unresponsive.
6. Do **not** merge unless explicitly asked.

## Checks

- Platforms that matter for the change still make sense (Pi / Nano / Mac / PC).
- Config/template changes preserve commented `myconfig` style.
- No secrets, credentials, or large binary tubs committed.
