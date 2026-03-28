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

def evaluate_with_claude(diff: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    
    prompt = f"""You are a deterministically strict Senior Code Review Agent.
Analyze the following .patch / diff.
Your goal is to mathematically deconstruct the code for:
1. Architectural Anti-patterns (e.g., lazy type padding).
2. Logical bugs or race conditions.
3. Security edge-cases.

If the PR is flawless, output "LGTM" and optionally praise the elegance.
Otherwise, provide a highly structured Markdown response detailing exact file corrections.

DIFF:
{diff}
"""

    payload = {
        "model": "claude-3-5-sonnet-20241022",
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
    parser.add_argument("--repo", required=True, help="GitHub repository (e.g., 'owner/repo')")
    parser.add_argument("--pr", required=True, type=int, help="Pull Request number")
    
    args = parser.parse_args()
    
    print(f"[*] Fetching Diff for {args.repo}#{args.pr}...")
    diff = fetch_pr_diff(args.repo, args.pr)
    
    if not diff.strip():
        print("[*] PR is empty. Nothing to review.")
        sys.exit(0)
        
    print("[*] Dispatching diff to Claude 3.5 Sonnet for Evaluation...")
    review_text = evaluate_with_claude(diff)
    
    print("[*] Writing analysis back to GitHub...")
    post_pr_comment(args.repo, args.pr, review_text)

if __name__ == "__main__":
    main()
