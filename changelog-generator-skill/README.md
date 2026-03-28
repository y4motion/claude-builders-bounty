# 📜 Absolute CHANGELOG Generator Skill

A precise, zero-dependency Python tool built for autonomous AI agents (like Claude Code) to easily generate structured, readable `CHANGELOG.md` files from raw Git history.

## Why this exists?
Coding agents often struggle to manually format changelogs by iterating through individual commit hashes. This tool abstracts the Git log formatting logic—parsing Conventional Commits (`feat:`, `fix:`, `chore:`) natively and printing them in an aesthetic Markdown structure.

Claude (or any autonomous agent) simply calls this script, reads the `stdout` as markdown, and either persists it or reports it back to the developer.

## Features
- **Deterministic Grouping:** Automatically categorizes commits into `✨ Features`, `🐛 Bug Fixes`, `♻️ Refactoring`, etc.
- **Timeframe Filtering:** Supports `--since "1 week ago"` or specific dates.
- **OpSec Proof:** Pure python, no `node_modules`, no brittle regex dependencies.

## Usage in Claude Code

You can instruct Claude to use this script by adding it to your workspace tools or `.claude` configuration.

### Command Line Intercept Example:
```bash
python generate_changelog.py --since "2 days ago" 
```

*Output:*
```markdown
# CHANGELOG

*Generated automatically on 2026-03-28*

## ✨ Features
- **76167ce** Add Zero-Trust Bash Pre-Tool Hook (y4motion)

## 🐛 Bug Fixes
- **a546d81** Correct typo in README (y4motion)
```

## Adding to an AI Agent's Workflow
Simply mount `generate_changelog.py` as an executable tool. The LLM can dynamically write the output to a file:
```bash
python generate_changelog.py > CHANGELOG.md
```

*Architected with precision by the Ghost Mod Team.*
