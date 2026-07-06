# LLM Contract Guard

Validate messy LLM JSON outputs against explicit response contracts.

![LLM Contract Guard cover](assets/readme-cover.svg)

## Where things live

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
```

## Processing path

![Workflow diagram](assets/readme-diagram.svg)

## Start here

```bash
git clone https://github.com/mertefekurt/llm-contract-guard.git
cd llm-contract-guard
python -m pip install -e ".[dev]"
llm-contract-guard examples/classifier.schema.json
```

## Useful details

- Designed as a focused model evaluation repo.
- Keeps setup short.
- Prioritizes readable output over infrastructure.
