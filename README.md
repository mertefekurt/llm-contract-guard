# LLM Contract Guard

![LLM Contract Guard cover](assets/readme-cover.svg)

## What I keep this for

Validate messy LLM JSON outputs against explicit response contracts.

It is a small repo, so the README focuses on the path from clone to first useful output.

## Clone and run

```bash
git clone https://github.com/mertefekurt/llm-contract-guard.git
cd llm-contract-guard
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
llm-contract-guard examples/classifier.schema.json
```

## Checks before changing it

```bash
ruff check .
pytest
python -m llm_contract_guard --help
```
