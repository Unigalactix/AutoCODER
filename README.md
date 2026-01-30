# Jira & GitHub Automation Workflow

This Python workflow automates the interaction between Jira and GitHub. It retrieves ticket details, analyzes repositories, manages Pull Requests, and reports back to Jira.

## Features

1.  **Jira Integration**: Fetches ticket details and posts comments.
2.  **Repo Analysis**: Scans for language, basic vulnerability checks (mock), and existing workflows.
3.  **GitHub Automation**: Creates branches, commits changes, and opens Pull Requests.
4.  **Workflow Monitoring**: Checks the status of GitHub Actions on the PR.

## Prerequisites

- Python 3.8+
- A Jira Account (Cloud)
- A GitHub Account

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment Variables**:
    Ensure your `.env` file contains the following keys (it already exists, just make sure values are correct):
    ```env
    JIRA_BASE_URL=https://your-domain.atlassian.net
    JIRA_USER_EMAIL=your-email@example.com
    JIRA_API_TOKEN=your-jira-api-token
    GITHUB_TOKEN=your-github-personal-access-token
    ```

## Usage

Run the main script:

```bash
python main.py
```

Follow the interactive prompts:
1.  Enter the **Jira Ticket ID** (e.g., `PROJ-101`).
2.  Enter the **GitHub Repository** name (e.g., `username/repo`).
3.  The script will perform the actions and wait for your confirmation to check the final workflow status.

## Workflow Details

- **Analysis**: The script posts a repository analysis summary to the Jira ticket.
- **PR Creation**: It creates a branch named `issue/<ticket-id>-fix` and adds a dummy file `automated_update.txt`.
- **Completion**: After you press Enter (simulating approval/merge), it checks for any Check Runs on the PR/Commit and posts the status back to Jira.
