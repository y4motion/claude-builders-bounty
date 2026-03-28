# Absolute Sentinel: Bash Pre-Tool Hook 🛡️

A zero-trust, deterministic pre-execution interceptor designed to prevent autonomous AI agents (like Claude Code) from executing destructive or irreversible terminal commands. 

This hook acts as a final safety layer between an LLM's raw intent and your local filesystem.

## Why this exists?
Autonomous coding agents are powerful, but occasionally suffer from hallucinatory paths that can lead them to execute `rm -rf /` or rewrite critical `.git` paths indiscriminately while trying to "clean up." 

**Absolute Sentinel** intercepts the exact command string *before* execution and parses it against a rigorous set of architectural constraints.

## Features
- **Deterministic Blockades:** Prevents `sudo`, reverse-shells (`/dev/tcp`), and destructive recursions (`rm -rf *`).
- **Dynamic Configuration:** Auto-generates `hook_config.json` on first run, allowing you to selectively toggle network blocking, FS mutations, and more.
- **Zero Dependencies:** Written in pure, semantic Python. No `pip install` required.

## Installation & Usage

1. **Clone & Setup:**
   ```bash
   chmod +x pre_tool_hook.py
   ```

2. **Integration with Claude Code (or any MCP Client):**
   Most modern AI agent frameworks allow you to configure a "pre-execution hook." Point the hook parameter to this script.
   
   Example usage in a bash wrapper:
   ```bash
   #!/bin/bash
   # agent_wrapper.sh
   TARGET_COMMAND="$1"
   
   if ./pre_tool_hook.py "$TARGET_COMMAND"; then
       eval "$TARGET_COMMAND"
   else
       echo "Execution blocked by Absolute Sentinel."
       exit 1
   fi
   ```

## Configuration (`hook_config.json`)
Upon the first run, a config file is generated:

```json
{
    "block_sudo": true,
    "block_destructive_rm": true,
    "block_fs_mutations": true,
    "block_network_exfiltration": false,
    "allowed_commands": ["ls", "cat", "pwd", "git", "grep", "echo"]
}
```

*Architected with precision by the Ghost Mod Team.*
