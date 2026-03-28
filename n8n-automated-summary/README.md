# Anthropic n8n Workflow: Weekly GitHub Repository Summary

This repository contains the exportable `n8n` workflow JSON that perfectly maps to the acceptance criteria for Anthropic Issue #5 ($200 Bounty).

## Acceptance Criteria Met
- [x] Exportable n8n workflow (`D1026_Claude_Automated_Summary.json`)
- [x] Trigger: weekly cron (Friday at 5pm) 
- [x] Fetches from GitHub API: commits, closed issues, merged PRs for the week
- [x] Calls Claude API (`claude-3-5-sonnet`) to generate a narrative summary
- [x] Delivers the summary via Discord webhook
- [x] Configurable variables: GitHub repo, destination channel, language (EN/FR)

## Setup Instructions (5 simple steps)

1. **Import Workflow:** Open your n8n workspace, click **Workflows** -> **Add Workflow** -> **Import from File**, and select `D1026_Claude_Automated_Summary.json`.
2. **Configure Anthropic Credentials:** Double-click the `Claude 3.5 Sonnet` node, select "Create New Credential", and input your Anthropic API Key.
3. **Set Configuration Variables:** Double-click the `Config Variables` node. You can securely adjust the `GITHUB_REPO` (e.g. `anthropic/anthropic-sdk-python`), the `DISCORD_WEBHOOK_URL`, and your preferred `SUMMARY_LANGUAGE` (`EN` or `FR`).
4. **Test the Workflow:** Click **Execute Workflow** at the bottom of the screen to trigger a manual test run immediately.
5. **Activate the Cron:** Toggle the workflow switch to **Active** in the top right corner. The workflow will now automatically run every Friday at 5 PM!

Enjoy your automated weekly engineering summaries powered by Claude 3.5 Sonnet!
