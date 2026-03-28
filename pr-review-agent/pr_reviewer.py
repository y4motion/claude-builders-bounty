#!/usr/bin/env python3
"""
Absolute PR Reviewer Sub-Agent
A zero-dependency (raw urllib) autonomous pipeline that fetches a GitHub PR diff,
executes a deterministic code review using Claude 3.5 Sonnet, and posts the architectural
feedback directly to the PR.

Usage:
  export GITHUB_TOKEN="ghp_xxx"
  export ANTHROPIC_API_KEY="sk-ant-xxx"
  python3 pr_reviewer.py --repo "owner/repo" --pr 123
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import re

def env_var(name):
    val = os.getenv(name)
    if not val:
        print(f"[FATAL] Missing required environment variable: {name}")
        sys.exit(1)
    return val

GITHUB_TOKEN = env_var("GITHUB_TOKEN")
ANTHROPIC_KEY = env_var("ANTHROPIC_API_KEY")

def fetch_pr_diff(repo: str, pr_num: int) -> str:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_num}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
        "X-GitHub-Api-Version": "2022-11-28"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"[FATAL] Failed to fetch PR diff: {e}")
        sys.exit(1)

def evaluate_with_claude(diff: str, model: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    
    prompt = f"""You are a strict PR Review Agent. Analyze the following patch/diff.
You MUST output precisely in this structured Markdown format and nothing else.

### Summary of changes
(2-3 sentences summarizing the exact modifications)

### Identified risks
* (List critical logic, type, or security risks)
* (If none, state "None detected")

### Improvement suggestions
* (List architectural or performance improvements)

### Confidence score: (Low / Medium / High)

DIFF:
{diff}
"""

    payload = {
        "model": model,
        "max_tokens": 2000,
        "temperature": 0.0,
        "system": "You are a pragmatic, zero-trust Code Review Sub-Agent. Speak clearly, concisely, and technically. No fluff.",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            return res_json['content'][0]['text']
    except urllib.error.URLError as e:
        err_msg = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        print(f"[FATAL] Anthropic API Error: {err_msg}")
        sys.exit(1)

def post_pr_comment(repo: str, pr_num: int, body: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_num}/comments"
    payload = {"body": f"🤖 **Absolute Review Agent (Claude 3.5)**\n\n{body}"}
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(f"[SUCCESS] Review posted! URL: {res.get('html_url')}")
    except urllib.error.URLError as e:
        print(f"[FATAL] Failed to post comment: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Claude PR Review Sub-Agent")
    parser.add_argument("--pr", required=True, help="GitHub Pull Request URL (e.g., https://github.com/owner/repo/pull/123)")
    parser.add_argument("--model", default=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"), help="Anthropic model to use (default: claude-3-5-sonnet-20241022)")
    parser.add_argument("--dry-run", action="store_true", help="Print the review to stdout instead of posting it")
    
    args = parser.parse_args()
    
    # Parse the GitHub URL based on Acceptance Criteria
    match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", args.pr)
    if not match:
        print("[FATAL] Invalid PR URL format. Expected: https://github.com/owner/repo/pull/123")
        sys.exit(1)
        
    owner, repo, pr_num_str = match.groups()
    repo_full = f"{owner}/{repo}"
    pr_num = int(pr_num_str)
    
    print(f"[*] Fetching Diff for {repo_full}#{pr_num}...")
    diff = fetch_pr_diff(repo_full, pr_num)
    
    if not diff.strip():
        print("[*] PR is empty. Nothing to review.")
        sys.exit(0)
        
    print(f"[*] Dispatching diff to {args.model} for Evaluation...")
    review_text = evaluate_with_claude(diff, args.model)
    
    if args.dry_run:
        print("\n" + "="*50 + "\n" + review_text + "\n" + "="*50 + "\n")
    else:
        print("[*] Writing analysis back to GitHub...")
        post_pr_comment(repo_full, pr_num, review_text)

if __name__ == "__main__":
    main()
