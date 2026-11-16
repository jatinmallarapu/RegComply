# RegComply

[![CI](https://github.com/jatinmallarapu/RegComply/actions/workflows/ci.yml/badge.svg)](https://github.com/jatinmallarapu/RegComply/actions/workflows/ci.yml)

Find source-backed rule passages, mask common identifiers in plain-text reviews, and compare explicitly provided rule versions.

## Architecture

```text
Question or document → identifier masking → lexical ranking → cited evidence
```

## Verification

| Scope | What the tests cover |
| --- | --- |
| Local acceptance tests | Cited retrieval, out-of-scope detection, PII masking, and version comparison |
| Production benchmark | Pending |

## Quickstart

Python 3.11 or newer.

```sh
python regcomply.py ask "What does FINRA say about misleading advertising?"
python -m pip install -e '.[dev]'
make test
```

## Design and data

The example corpus contains two hand-written reference summaries with links to FINRA. The summaries are not quotations. FINRA source material is governed by its own terms. [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210) · [FINRA Rule 3110](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110)

[Requirements](specs/core/requirements.md) · [Design](specs/core/design.md) · [Tasks](specs/core/tasks.md)

[Architecture decision](docs/adr/0001-local-baseline.md)

## Remaining milestones

Bedrock Knowledge Bases, LangGraph, MCP, A2A, PDF review, tracing, EKS, and a reviewed golden set.
