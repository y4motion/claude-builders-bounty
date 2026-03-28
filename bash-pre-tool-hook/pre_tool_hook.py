#!/usr/bin/env python3
"""
Absolute Sentinel: Bash Pre-Tool Hook
A deterministic, zero-trust interceptor for autonomous AI bash command execution.

Usage in Claude Code / AI Agents:
  Configure your agent to run this hook before executing any `bash` or `shell` tool.
  If this script exits with status `1`, the agent is blocked from executing the command.
  If it exits with status `0`, execution proceeds.
"""

import sys
import re
import os
import json
from pathlib import Path

CONFIG_PATH = Path("hook_config.json")

DEFAULT_CONFIG = {
    "block_sudo": True,
    "block_destructive_rm": True,
    "block_fs_mutations": True,
    "block_network_exfiltration": False,
    "allowed_commands": ["ls", "cat", "pwd", "git", "grep", "echo"]
}

def load_config():
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    try:
        return json.loads(CONFIG_PATH.read_text())
    except:
        return DEFAULT_CONFIG

def analyze_command(cmd: str, config: dict) -> tuple[bool, str]:
    cmd_lower = cmd.lower().strip()
    
    # 1. Trivial pass
    if not cmd_lower:
        return True, "Empty command"
        
    # 2. Sudo block
    if config.get("block_sudo") and re.search(r'\bsudo\b', cmd_lower):
        return False, "SUDO execution is explicitly blocked."
        
    # 3. Destructive RM block
    if config.get("block_destructive_rm"):
        if re.search(r'rm\s+.*-r.*f', cmd_lower) or re.search(r'rm\s+.*-f.*r', cmd_lower):
            if "/" in cmd_lower or "*" in cmd_lower:
                return False, "Destructive `rm -rf` with wildcards/root paths blocked."
                
    # 4. Filesystem low-level mutations
    if config.get("block_fs_mutations"):
        dangerous_fs = ['mkfs', 'dd ', 'fdisk', 'mkswap', 'chmod -R 777']
        for danger in dangerous_fs:
            if danger in cmd_lower:
                return False, f"Low-level filesystem mutation `{danger}` blocked."
                
    # 5. Reverse shell / Network exfiltration (Heuristic)
    if config.get("block_network_exfiltration"):
        exfil_patterns = [r'/dev/tcp/', r'nc -e', r'curl.*\| bash', r'wget.*\| sh']
        for pat in exfil_patterns:
            if re.search(pat, cmd_lower):
                return False, "Potential reverse-shell or untested network exec blocked."
                
    return True, "Command cleared."

def main():
    if len(sys.argv) < 2:
        print("[SENTINEL] Error: No command provided to hook.")
        sys.exit(1)
        
    target_cmd = sys.argv[1]
    config = load_config()
    
    allowed, reason = analyze_command(target_cmd, config)
    
    if not allowed:
        print(f"\n[SENTINEL_BLOCK] Command rejected by Pre-Tool Hook.")
        print(f"[REASON] {reason}")
        print(f"[TARGET] {target_cmd}\n")
        sys.exit(1) # Block agent execution

    sys.exit(0) # Allow execution

if __name__ == "__main__":
    main()
