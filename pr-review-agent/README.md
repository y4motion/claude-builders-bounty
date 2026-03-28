# Absolute PR Review Agent 🦅

A zero-dependency, ultra-lightweight autonomous sub-agent designed for the Claude ecosystem. This script natively binds the GitHub API to Anthropic's `claude-3-5-sonnet` to perform rigorous, deterministic code reviews directly on Pull Requests.

## Why this agent?
Standard reviewing agents require heavy SDKs (`requests`, `PyGithub`, `anthropic`). They break easily in restricted environments (like CI/CD runners or AI sandboxes).
**This Absolute Agent** is written purely with Python's standard library (`urllib`). It executes in milliseconds, requires zero `requirements.txt`, and operates seamlessly inside any Alpine container or restricted Claude Code environment.

## Execution Flow
1. Computes the raw `vnd.github.v3.diff` from the target PR.
2. Pipes the diff directly to `api.anthropic.com` under an elite Senior Architect persona.
3. Automatically posts the structured Markdown critique as a top-level GitHub comment.

## Usage (CLI / Claude Code Hook)

Ensure you have your keys exported:
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxx"
```

Then invoke the sub-agent via standard CLI routing:
```bash
python pr_reviewer.py --repo "claude-builders-bounty/claude-builders-bounty" --pr 123
```

## GitHub Actions Integration
You can wrap this single script in a `.yml` workflow natively to trigger on `pull_request` events without Docker or external marketplace actions.

*Architected with zero-trust principles by the Ghost Mod Team.*
