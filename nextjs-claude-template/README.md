# Professional Next.js + SQLite `CLAUDE.md` Template

A masterclass custom instructions file for Claude designed by a Senior Engineering Team to enforce deterministic architecture and zero-trust type safety in modern Next.js 14/15 App Router codebases.

## Why this template?

Most `CLAUDE.md` templates provided in the community are overly permissive. This leads AI coding agents to:
- Fall back to generic `any` types.
- Misuse React Server Components (RSC) vs. Client Boundaries.
- Create lazy failure states (like `id: payload.id ?? 0` which corrupts DB integrity).

This `CLAUDE.md` template is engineered to enforce **Absolute Architecture**:
1. **RSC First:** Forces Claude to isolate client-side logic to the absolute minimum tree depth.
2. **Drizzle ORM + SQLite:** Defines specific patterns for querying and mutations via Server Actions.
3. **Ghost Mod Type Safety:** Strictly outlaws lazy padding, zero-value fallbacks, and `any`.

## Installation

1. Copy the `CLAUDE.md` file into the root of your Next.js project.
2. Ensure you have Claude Code or Claude.ai project knowledge synced.
3. Claude will automatically read these principles and adjust its architectural output to match elite team standards.

*Architected with precision by the Ghost Mod Team.*
