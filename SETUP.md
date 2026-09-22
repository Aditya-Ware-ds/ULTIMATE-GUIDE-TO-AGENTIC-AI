# Setup

You need Python 3.11+, [uv](https://docs.astral.sh/uv/), and git. No API keys are
required to work through the curriculum -- every lab's tests run offline against a
mock LLM provider. API keys are only needed if you choose to run a lab against a
real model (`make test-live`, or the "swap in a real provider" step in each lab).

## All platforms: install uv

`uv` manages the Python version, virtual environment, and dependencies for this
repo -- you don't need to install Python or create a venv by hand.

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify: `uv --version`. Full instructions (including package-manager installs) at
the [official uv docs](https://docs.astral.sh/uv/getting-started/installation/).

## Clone and install

```bash
git clone <this-repo>
cd agentic-ai-mastery
make setup    # uv sync --all-groups: installs runtime, dev, and docs dependencies
make test     # confirms the offline suite is green before you start
```

If you don't have `make`:
- **Windows without make:** install it via `winget install GnuWin32.Make` or use
  Git Bash / WSL, or just run the commands inside the `Makefile` directly with `uv run ...`.
- **macOS:** `make` ships with Xcode Command Line Tools (`xcode-select --install`).
- **Linux:** `make` is in your distro's default repos (`apt install make`, etc.).

## Optional: real provider API keys

Copy `.env.example` to `.env` and fill in only the providers you plan to use:

- **Anthropic:** key from [console.anthropic.com](https://console.anthropic.com/settings/keys)
- **OpenAI:** key from [platform.openai.com](https://platform.openai.com/api-keys)
- **Google Gemini:** key from [aistudio.google.com](https://aistudio.google.com/apikey)
- **Ollama (local, free):** install from [ollama.com](https://ollama.com/download), then
  `ollama pull qwen3:8b` (the curriculum's default local tool-calling model)

Real-provider labs show an estimated cost before you run them (see
`shared/llm/pricing.py`) and default to the cheapest current model per provider.

## Optional: browser automation (Module 14)

```bash
uv run playwright install chromium
```

## Editor setup

Any editor works. If you use VS Code, the Python and Ruff extensions will pick up
this repo's `pyproject.toml` config automatically.

## Troubleshooting

- **`uv sync` fails to build the project:** make sure you're running it from the
  repo root (where `pyproject.toml` and `README.md` live).
- **Tests fail on first run:** run `make lint` too -- a formatting/lint error can
  mask a real test failure in the output.
- **WSL/Windows line-ending diffs in `git status`:** this repo ships a
  `.gitattributes` normalizing line endings; if you still see whole-file diffs,
  run `git add --renormalize .`.
