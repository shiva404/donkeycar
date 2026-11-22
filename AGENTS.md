# AGENTS.md — Donkeycar

Guidance for AI agents and contributors working in this repo. Prefer this file and `.cursor/` over chat-only memory so the whole team shares the same defaults.

Also see: `CONTRIBUTING.md`, `PYTHON312_MIGRATION.md`, `README.md`, docs at https://docs.donkeycar.com

## What this project is

Modular Python self-driving library for hobbyists (DIY Robocars): Raspberry Pi / Jetson cars, simulators, and fast experimentation.

- Upstream: https://github.com/autorope/donkeycar
- CLI: `donkey` → `donkeycar.management.base:execute_from_command_line`
- Runtime: `Vehicle` drive loop + shared `Memory` key/value bus; behavior from **parts** and **templates**

## Repo map

| Path | Role |
|------|------|
| `donkeycar/vehicle.py` | Drive loop: schedules parts, profiling |
| `donkeycar/memory.py` | Shared key/value bus between parts |
| `donkeycar/parts/` | Cameras, controllers, actuators, ML, GPS, lidar, etc. |
| `donkeycar/templates/` | User apps + `cfg_*.py` / `myconfig.py` |
| `donkeycar/management/` | `donkey` CLI, UI, tub web tools |
| `donkeycar/pipeline/` | Training / data pipeline helpers |
| `donkeycar/tests/` | Pytest suite |
| `scripts/` | Utility scripts |
| `arduino/` | Encoder sketches |
| `pyproject.toml` | Package metadata, extras, console script |

## Mental model

1. Instantiate `Vehicle` (owns a `Memory`).
2. `V.add(part, inputs=[...], outputs=[...], threaded=?)` to build the loop.
3. `V.start(rate_hz=...)` runs parts in order each tick.
4. Log to **tubs**; train; drive with DL / CV / GPS path-follow autopilots.

## How we work

- Prefer small, reviewable PRs.
- Ask before merging, deploying, or publishing to PyPI.
- Never invent hardware behavior; check `donkeycar/parts/` and docs first.
- Support Raspberry Pi OS, Jetson Nano, Linux, macOS, WSL.
- Prefer editing existing parts/templates over one-off vehicle-loop forks.
- Keep `myconfig.py` / `cfg_*.py` commented-default style.
- New features should be broadly useful; niche hardware → fork unless discussed in an Issue.
- Unit tests for behavior changes; run `make tests` or `uv run pytest` before claiming green.
- PEP-8, avoid duplication, prefer classes over monolithic functions; no monkey-patching.
- User docs live in `autorope/donkeydocs` — note when a code change needs a docs PR.

## Python / tooling

- Python `>=3.12,<3.14`. Use **uv** (not conda).
- Extras: `[pi]` (Pi 3.13 + system-site-packages for libcamera), `[macos]` / `[pc]` (Python 3.12 + TF 2.19), `[nano]`, `[torch]`, `[dev]`.
- Mac/PC stay on 3.12 (TF 2.19 SavedModel broken on 3.13); Pi uses 3.13 for Debian `picamera2`.
- Read `PYTHON312_MIGRATION.md` before changing Python/TF/uv install guidance.
- Dev install: `uv pip install -e ".[<extra>,dev]"`

## Battery voltage

- Fastest: multimeter on LiPo main leads (2S ~7.4V nominal, 3S ~11.1V). Charge if &lt; ~3.5V/cell.
- On-car: INA219 on I2C (`donkeycar/parts/battery_monitor.py`). Default addr **0x41** (0x40 is PCA9685). `donkey battery` for a one-shot read; set `HAVE_BATTERY_MONITOR = True` in myconfig to log while driving.
- Pi `Undervoltage detected` is the **5V Pi rail**, not the traction pack.

## Xbox controller (Pi)

- Default template config: `CONTROLLER_TYPE = 'xbox'`, device `/dev/input/js0`.
- Bluetooth Xbox pads on Raspberry Pi OS often need `disable_ertm=1`, `uhid`, and **xpadneo** when stock `hid-generic` fails to probe (see `XboxOneJoystick` in `donkeycar/parts/controller.py`).
- Kernel headers package is `linux-headers-$(uname -r)` / `linux-headers-rpi-v8`, not the old `raspberrypi-kernel-headers`.
- Diagnose pad→Pi vs car throttle: `donkey xbox` (optional `--device`, `--config`, `--swapped`, `--raw`). If DRIVE throttle moves when you pull RT/stick, Xbox→Pi is fine — next check `donkey calibrate` / ESC / `donkey battery`.

## Agent workflows

Repeatable procedures live under `.cursor/workflows/`:

- [Dev setup](.cursor/workflows/dev-setup.md)
- [Run tests](.cursor/workflows/run-tests.md)
- [Ship a PR](.cursor/workflows/pr-shipping.md)
- [Add or change a part](.cursor/workflows/add-part.md)

Cursor rules (always-on principles) live under `.cursor/rules/`.
