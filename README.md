# Intern_GenAI_Examples

Practical AI webinar examples — basic LLM API calls (single prompts, batching, chat with/without memory, tool calls, embeddings) using LangChain and the OpenAI API.

There are two notebooks:

| Notebook | Use when... |
|---|---|
| `main.ipynb` | Working locally in VS Code |
| `main_colab.ipynb` | Working in Google Colab |

## Learning materials

Beyond the notebooks, this repo has extra training material:

| File | Covers |
|---|---|
| [`docs/claude_code_bash_git_commands.md`](docs/claude_code_bash_git_commands.md) (also as [PDF](docs/claude_code_bash_git_commands.pdf)) | Cheat sheet — Claude Code commands, Bash, Git |
| [`docs/setup_instructions.txt`](docs/setup_instructions.txt) (also as [PDF](docs/setup_instructions.pdf)) | Windows copy-paste setup commands |
| [`TASKS.md`](TASKS.md) | Daily practice tasks — quiz, Claude Code, Bash, LangChain API |

## Claude Code agents & skills

This repo is also set up to practise Claude Code's project-level automation, in `.claude/`:

| Type | Examples | Purpose |
|---|---|---|
| Agents (`.claude/agents/`) | `doc_extract_doer`, `doc_reviewer`, `doc_pipeline`, `oscar_doer`, `oscar_reviewer`, `oscar_pipeline` | Multi-step doer/reviewer/pipeline patterns for PDF metadata extraction and Oscar-winner analysis |
| Skills (`.claude/skills/`) | `dw_batch`, `actuarial-ml-paper-brief`, `create-practical-ai-slides`, `revise-practical-ai-slides`, `oscars-award-winners`, `ship-learn-next` | Reusable task recipes — `dw_batch` covers async/batch LLM processing |
| Commands (`.claude/commands/`) | project-specific slash commands | Manual shortcuts invoked with `/` |

## Option A: Google Colab (no setup)

Open `main_colab.ipynb` in [Google Colab](https://colab.research.google.com/). Add your `OPENAI_API_KEY` under Colab's **Secrets** (key icon in the left sidebar) — the notebook reads it from there. No local install needed.

## Option B: Running locally

### 1. Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [VS Code](https://code.visualstudio.com/) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions

### 2. Clone the repo

```bash
git clone https://github.com/NnamdiOdozi/Intern_GenAI_Examples.git
cd Intern_GenAI_Examples
```

### 3. Set up the environment

We recommend **uv** — it's faster than pip and installs the exact versions this project was built with. A `pip` fallback (using `requirements.txt`) is also provided below if you'd rather stick with what you know.

#### Using uv (recommended)

Install uv (one-time, skip if already installed):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create the virtual environment and install dependencies (run from the repo root):

```bash
uv venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv sync
```

`uv sync` reads `pyproject.toml` / `uv.lock` and installs everything at the pinned versions.

#### Using pip (fallback)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Generate a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) if you don't have one.

Copy the example env file and fill in your key:

```bash
cp .env.example .env
```

Open `.env` and set:

```
OPENAI_API_KEY=sk-...your-key-here...
```

`.env` is git-ignored, so your key stays local.

### 5. Open the notebook and select the kernel

Open the repo folder in VS Code (`code .` from the repo root, or File → Open Folder), then open `main.ipynb`.

**Before running any cells**, select the kernel: press **Ctrl+Shift+P** (Cmd+Shift+P on Mac) → **"Notebook: Select Notebook Kernel"** → **Python Environments** → pick the `.venv` in this repo folder (it'll be listed as `.venv (Python 3.12.x)` or similar). No manual registration needed — VS Code detects it automatically since `ipykernel` is already in the environment.

Alternatively, click the kernel name in the top-right corner of the notebook and pick `.venv` from the dropdown.

Then run the cells from the top.

## Troubleshooting

- **`ModuleNotFoundError` in the notebook** — wrong kernel selected. Ctrl+Shift+P → "Notebook: Select Notebook Kernel" → pick the `.venv` in this repo. If it's not listed, make sure step 3 finished without errors and reload the VS Code window (Ctrl+Shift+P → "Developer: Reload Window").
- **`OPENAI_API_KEY` not found / authentication error** — check `.env` exists in the repo root (not `.env.example`) and contains a valid key with no quotes or extra spaces.
- **`uv: command not found`** — close and reopen your terminal after installing uv, or add it to your `PATH` per the installer's output.
