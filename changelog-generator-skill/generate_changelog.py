#!/usr/bin/env python3
"""
Absolute CHANGELOG Generator
A deterministic Git Log parser designed to be consumed as a Claude Code Skill.

Usage:
  python3 generate_changelog.py [--since "1 week ago"] [--output CHANGELOG.md]
"""

import subprocess
import re
import argparse
import sys
from collections import defaultdict
from datetime import datetime

def run_git_log(since=None):
    cmd = ['git', 'log', '--pretty=format:%H|%s|%an|%ad', '--date=short']
    if since:
        cmd.extend(['--since', since])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error executing git log: {e.stderr}")
        sys.exit(1)

def parse_commits(commits):
    categories = defaultdict(list)
    
    # Conventional Commits regex
    pattern = re.compile(r'^(\w+)(?:\((.*)\))?!?: (.*)')
    
    for commit in commits:
        if not commit.strip():
            continue
            
        parts = commit.split('|', 3)
        if len(parts) != 4:
            continue
            
        hash_id, msg, author, date = parts
        match = pattern.match(msg)
        
        if match:
            type_tag = match.group(1).lower()
            scope = match.group(2)
            desc = match.group(3)
        else:
            type_tag = 'other'
            desc = msg
            
        categories[type_tag].append({
            'hash': hash_id[:7],
            'desc': desc,
            'author': author,
            'date': date
        })
        
    return categories

def generate_markdown(categories):
    lines = [f"# CHANGELOG", f"\n*Generated automatically on {datetime.now().strftime('%Y-%m-%d')}*\n"]
    
    type_headers = {
        'feat': '✨ Features',
        'fix': '🐛 Bug Fixes',
        'docs': '📚 Documentation',
        'refactor': '♻️ Refactoring',
        'perf': '⚡ Performance',
        'chore': '🧹 Chores & Maintenance',
        'other': '📦 Other Changes'
    }
    
    # Sort categories by importance
    order = ['feat', 'fix', 'perf', 'refactor', 'docs', 'chore', 'other']
    
    for cat in order:
        if cat in categories and categories[cat]:
            lines.append(f"## {type_headers.get(cat, type_headers['other'])}")
            for commit in categories[cat]:
                lines.append(f"- **{commit['hash']}** {commit['desc']} ({commit['author']})")
            lines.append("")
            
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Deterministic CHANGELOG Generator for Claude Code")
    parser.add_argument("--since", help="Timeframe (e.g., '1 week ago', '2023-01-01')", default=None)
    parser.add_argument("--output", help="Write to file instead of stdout", default=None)
    
    args = parser.parse_args()
    
    commits = run_git_log(args.since)
    if not commits or not commits[0]:
        print("No commits found in the specified timeframe.")
        sys.exit(0)
        
    structured_data = parse_commits(commits)
    markdown_output = generate_markdown(structured_data)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print(f"CHANGELOG successfully written to {args.output}")
    else:
        print(markdown_output)

if __name__ == "__main__":
    main()
