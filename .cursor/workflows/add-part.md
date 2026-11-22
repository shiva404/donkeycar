# Workflow: Add or change a part

**When:** New sensor/actuator/autopilot helper, or changing part I/O.
**Result:** A part that fits the Vehicle loop and is wired (or documented) in a template.

## Steps

1. Read `AGENTS.md` and an existing similar part under `donkeycar/parts/`.
2. Part contract: `run(*inputs)` (and optional `update`/`run_threaded`/`shutdown` for threaded parts).
3. Declare clear Memory keys; wire via `Vehicle.add(..., inputs=[...], outputs=[...], threaded=...)`.
4. Prefer updating a template under `donkeycar/templates/` + matching `cfg_*.py` rather than only showing a snippet.
5. Add/adjust unit tests; keep hardware access behind interfaces where possible.
6. If user-facing, note a docs change for `autorope/donkeydocs`.

## Checks

- Does not break the drive loop rate (avoid blocking work on the main loop without `threaded=True`).
- Types/shapes of Memory values match consumers (images, floats for steer/throttle, etc.).
