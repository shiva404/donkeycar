# Workflow: Dev setup

**When:** First clone, new machine, or broken env.
**Result:** Editable install with tests runnable.

## Steps

1. Confirm Python target for the platform:
   - Mac/PC: 3.12
   - Raspberry Pi (Trixie): 3.13 + `sudo apt install python3-libcamera python3-picamera2`
2. Create venv with uv:
   - Mac: `uv venv ~/.venvs/donkeycar --python 3.12`
   - PC: same as Mac
   - Pi: `uv venv ~/env --python 3.13 --system-site-packages`
3. Activate and install:
   - Mac: `uv pip install -e ".[macos,dev]"`
   - PC: `uv pip install -e ".[pc,dev]"`
   - Pi: `uv pip install -e ".[pi,dev]"`
4. Sanity: `donkey --help` (or `python -m donkeycar.management.base --help`), then `uv run pytest` / `make tests`.

## Checks

- `pyproject.toml` extras match the platform.
- Do not recommend conda; see `PYTHON312_MIGRATION.md` if changing install docs.
