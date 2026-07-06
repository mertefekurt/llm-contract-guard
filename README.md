![LLM Contract Guard cover](assets/readme-cover.svg)

# LLM Contract Guard

![stack](https://img.shields.io/badge/stack-Python-be185d?style=flat-square) ![python](https://img.shields.io/badge/python-3.11-4b5563?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-2563eb?style=flat-square) ![ci](https://img.shields.io/badge/ci-GitHub%20Actions-16a34a?style=flat-square)

Validate messy LLM JSON outputs against explicit response contracts.

## Read this first

This is a compact tool, not a platform. The useful part is the repeatable check and the plain output, so the repository keeps setup and code paths short.

## First run

```bash
python -m pip install -e ".[dev]"
llm-contract-guard examples/classifier.schema.json
```

## Maintenance

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m llm_contract_guard --help
```

## Repository map

```text
.github/        CI workflow
examples/       sample inputs
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
