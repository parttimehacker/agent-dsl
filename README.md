# Agent DSL

A minimal open-source starter for a domain-specific language designed for AI agents such as ChatGPT and Claude.

This repository turns the design idea into a working prototype:

- a small YAML-based workflow spec
- a Python runtime
- typed validation hooks
- deterministic tool execution
- model-step stubs for future LLM integration
- examples and tests

## Why this exists

Prompt-only systems are flexible, but they are hard to validate, inspect, and govern. Agent DSL is a lightweight attempt to separate:

- **intent**
- **execution**
- **reasoning**
- **policy**
- **output contracts**

The goal is not to replace Python. The goal is to give AI workflows a structured language that is easier to debug and safer to operate.

## Core ideas

Agent DSL treats an AI workflow as a contract between:

1. **Human intent** — what the workflow is trying to accomplish
2. **Machine execution** — what tools are allowed to do
3. **Model cognition** — where LLMs perform fuzzy tasks such as synthesis
4. **Governance** — what constraints and checks must hold

It also leaves room for a future epistemic layer where outputs can carry:

- evidence
- confidence
- uncertainty
- conflict markers

## Repository layout

```text
agent-dsl-repo/
├── agent_dsl/
│   ├── __init__.py
│   ├── cli.py
│   ├── engine.py
│   ├── exceptions.py
│   ├── models.py
│   ├── runner.py
│   ├── tools.py
│   └── validators.py
├── docs/
│   └── whitepaper-outline.md
├── examples/
│   ├── ai_protocol_brief.yaml
│   └── structurehub_signal_check.yaml
├── tests/
│   └── test_engine.py
├── pyproject.toml
└── README.md
```

## Workflow format

The first public version uses YAML instead of a custom parser. That keeps the implementation small and lets the semantics mature before inventing syntax.

A workflow has five main parts:

- `goal`
- `inputs`
- `policy`
- `steps`
- `output`

Example:

```yaml
name: ai_protocol_brief
goal: Create a short briefing on recent AI protocol initiatives

inputs:
  topic: AI-to-AI communication protocols
  audience: enterprise IT leaders

policy:
  max_tool_calls: 5
  require_non_empty_output: true

steps:
  - name: collect_articles
    kind: tool
    tool: search_web
    args:
      query: "${inputs.topic}"
    bind: articles

  - name: summarize
    kind: model
    instruction: Summarize the article list into a concise executive brief.
    source: articles
    bind: summary

output:
  variable: summary
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install the package

```bash
pip install -e .
```

### 3. Run an example workflow

```bash
agent-dsl run examples/ai_protocol_brief.yaml
```

## Current runtime behavior

The runtime supports two step kinds:

### Tool step
Runs a registered Python tool deterministically.

### Model step
Runs a placeholder model adapter. Right now it is intentionally simple so the repository remains usable without an API key.

## Built-in example tools

- `search_web` — stubbed search function returning deterministic sample items
- `echo` — returns the provided input
- `structurehub_check` — demonstrates how a domain tool might inspect sensor values

These are scaffolding tools. They are meant to show architecture, not replace production integrations.

## Example use cases

### Research workflow
The `ai_protocol_brief.yaml` example shows how a research assistant can collect information and summarize it.

### IoT / StructureHub workflow
The `structurehub_signal_check.yaml` example shows how a workflow can inspect sensor values and produce a structured interpretation.

This is where the idea becomes practical: the same language can orchestrate web research, document review, and sensor analysis.

## Roadmap

### v0.1
- YAML workflow format
- core runtime
- deterministic tool registry
- output checks

### v0.2
- JSON Schema or Pydantic output validation
- retries and fallback branches
- richer variable interpolation

### v0.3
- model adapters for OpenAI and Anthropic
- trace logging
- cost accounting
- policy enforcement improvements

### v1.0
- custom DSL syntax
- parser + AST
- typed workflow definitions
- epistemic annotations for evidence and confidence

## Philosophy

Traditional programming languages assume exact execution and deterministic state changes.

AI workflows are different. They mix:

- exact computation
- probabilistic synthesis
- incomplete information
- real-world constraints

That is why a language for AI agents should be understood not only as a programming language, but also as a **contract language for intention, action, and knowledge**.

## Publishing this as a public repo

A good first public GitHub description would be:

> A minimal YAML-first workflow language and runtime for AI agents, designed to make prompt-based systems more structured, inspectable, and governable.

Suggested tags:

- ai
- agents
- workflow
- dsl
- llm
- orchestration
- python

## License

MIT

