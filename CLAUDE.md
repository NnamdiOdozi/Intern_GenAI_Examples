# Intern_GenAI_Examples

## Purpose and audience

This repository contains practical, educational GenAI examples for interns and webinar participants. Prefer clear, approachable examples and explanations that help learners understand what each step is doing.

## Primary entry points

- `main.ipynb` is the notebook for local use in VS Code.
- `main_colab.ipynb` is the Google Colab version.
- `README.md` contains setup and usage guidance.
- `TASKS.md` contains practice exercises.
- When changing shared examples, check whether both notebooks need the corresponding update.

## Environment and dependencies

- The project requires Python 3.12 or later.
- Prefer `uv` with `pyproject.toml` and `uv.lock`; `requirements.txt` is the fallback installation path.
- The project uses direnv through `.envrc`. If environment variables are missing, check that direnv is installed and `.envrc` has been allowed.
- Secrets belong in `.env` and must not be committed.

## Project agents and skills

- Project-specific agents are under `.claude/agents/`.
- Project-specific skills are under `.claude/skills/`; read the relevant `SKILL.md` before using one.
- For asynchronous bulk document or data processing, use `.claude/skills/dw_batch/`. Its standard output directory is `dw_batch_output/`.

## Data and outputs

- `ifoa_downloads/` contains source documents and supporting files for the IFoA paper workflow.
- `output/` contains generated reports, tables, diagrams, and other reviewed outputs.
- Do not overwrite source documents when producing derived or reviewed artifacts.
