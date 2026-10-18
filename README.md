# Llm Contract Guard

![Llm Contract Guard cover](assets/readme-cover.svg)

Validate messy LLM JSON outputs against explicit response contracts.

`Python`

## Start here

```bash
git clone https://github.com/mertefekurt/llm-contract-guard.git
cd llm-contract-guard
python -m pip install -e ".[dev]"
llm-contract-guard examples/classifier.schema.json
```

## Project map

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
```

## Repository

[Open the source on GitHub →](https://github.com/mertefekurt/llm-contract-guard)

[MIT License](LICENSE)
