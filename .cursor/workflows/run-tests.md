# Workflow: Run tests

**When:** Before claiming a fix/feature is done, or after dependency changes.
**Result:** Known pytest outcome for touched areas (full suite when feasible).

## Steps

1. From repo root: `make tests` or `uv run pytest`.
2. For a focused change: `uv run pytest path/to/test_file.py -q`.
3. Coverage config lives in `.coveragerc` if measuring coverage.
4. Report what actually ran — never claim tests you did not execute.

## Checks

- New behavior has a unit test under `donkeycar/tests/`.
- Hardware-dependent parts: prefer mocks/`responses`; do not require a Pi to unit-test pure logic.
