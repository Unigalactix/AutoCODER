import os
import sys
from dotenv import load_dotenv
from src.jira_handler import JiraHandler
from src.github_handler import GithubHandler
from src.analyzer import analyze_repo

def main():
    # 1. Load Environment Variables
    load_dotenv()
    
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
    JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    # Simple check
    if not all([JIRA_BASE_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN, GITHUB_TOKEN]):
        print("Error: Missing one or more required environment variables.")
        print("Ensure JIRA_BASE_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN, and GITHUB_TOKEN are set in .env")
        return

    # Initialize Handlers
    jira = JiraHandler(JIRA_BASE_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)
    github = GithubHandler(GITHUB_TOKEN)

    # 2. Get Ticket Input
    ticket_id = input("Enter Jira Ticket ID (e.g., PROJ-123): ").strip()
    if not ticket_id:
        print("Ticket ID is required.")
        return

    print(f"Fetching details for {ticket_id}...")
    ticket_details = jira.get_ticket_details(ticket_id)
    if not ticket_details:
        return

    print(f"Ticket Summary: {ticket_details['summary']}")
    
    # 3. GitHub Operations - Repository Selection
    # For this workflow, we assume the repo name is either derived from the ticket or requested.
    # Let's ask the user for the repo name for flexibility.
    repo_name = input("Enter GitHub Repository (owner/repo): ").strip()
    
    print(f"Verifying access to {repo_name}...")
    repo = github.verify_access(repo_name)
    if not repo:
        return

    # 4. Analyze & Report
    print("Analyzing repository...")
    analysis = analyze_repo(repo)
    
    report_comment = (
        f"h2. Automated Repository Analysis for {repo_name}\n\n"
        f"*Language:* {analysis['language']}\n"
        f"*Potenital Vulnerabilities:* {', '.join(analysis['vulnerabilities'])}\n"
        f"*Existing Workflows:* {', '.join(analysis['workflows'])}"
    )
    
    print("Posting analysis report to Jira...")
    jira.post_comment(ticket_id, report_comment)

    # 5. Create Pull Request
    branch_name = f"issue/{ticket_id.lower()}-fix"
    print(f"Creating branch {branch_name}...")
    if github.create_branch(repo, branch_name):
        
        # Make a dummy code modification
        print("Making code modifications...")
        github.create_file_update(
            repo, 
            branch_name, 
            "automated_update.txt", 
            f"Automated update for ticket {ticket_id}", 
            f"Fix for {ticket_id}"
        )
        
        pr_title = f"{ticket_id}: {ticket_details['summary']}"
        pr_body = f"Automated PR for Jira Ticket: {ticket_id}\n\n{ticket_details['description']}"
        
        pr = github.create_pull_request(repo, branch_name, pr_title, pr_body)
        
        if pr:
            jira.post_comment(ticket_id, f"Pull Request created: {pr.html_url}")
            
            # 6. Await User Review
            print(f"PR created: {pr.html_url}")
            input("Press Enter after you have reviewed/approved the PR code (simulation)...")
            
            # 7. Check Workflow
            status_report = github.check_workflow_status(repo, pr.number)
            
            final_comment = f"h2. Post-Approval Workflow Status\n\n{status_report}"
            jira.post_comment(ticket_id, final_comment)
            print("Done. Workflow status posted to Jira.")

if __name__ == "__main__":
    main()
