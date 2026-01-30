from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

from src.jira_handler import JiraHandler
from src.github_handler import GithubHandler
from src.analyzer import analyze_repo

# Load environment variables
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize handlers
jira = JiraHandler(JIRA_BASE_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)
github = GithubHandler(GITHUB_TOKEN)

# Initialize MCP Server
mcp = FastMCP("AutoCODER Server")

@mcp.tool()
def get_jira_ticket(ticket_id: str) -> str:
    """Retrieves details for a specific Jira ticket."""
    details = jira.get_ticket_details(ticket_id)
    if details:
        return f"Ticket {details['key']}: {details['summary']}\nStatus: {details['status']}\nDescription: {details['description']}"
    return "Ticket not found or error occurred."

@mcp.tool()
def post_jira_comment(ticket_id: str, comment: str) -> str:
    """Posts a comment to a Jira ticket."""
    if jira.post_comment(ticket_id, comment):
        return f"Successfully posted comment to {ticket_id}"
    return "Failed to post comment."

@mcp.tool()
def analyze_github_repo(repo_name: str) -> str:
    """Analyzes a GitHub repository for language and issues."""
    repo = github.verify_access(repo_name)
    if not repo:
        return "Could not access repository."
    
    analysis = analyze_repo(repo) 
    # Note: We aren't passing the internal LLM handler here because 
    # the Agent calling this tool likely has its own LLM capabilities!
    
    return (
        f"Language: {analysis['language']}\n"
        f"Vulnerabilities: {', '.join(analysis['vulnerabilities'])}\n"
        f"Workflows: {', '.join(analysis['workflows'])}"
    )

@mcp.tool()
def create_branch_and_pr(ticket_id: str, repo_name: str, pr_title: str, pr_body: str, change_description: str) -> str:
    """
    Creates a branch, pushes a dummy update (simulation), and opens a PR.
    """
    repo = github.verify_access(repo_name)
    if not repo:
        return "Repo access failed."

    branch_name = f"issue/{ticket_id.lower()}-fix"
    if not github.create_branch(repo, branch_name):
        return "Branch creation failed."

    # Create dummy file update
    github.create_file_update(
        repo, 
        branch_name, 
        "manual_mcp_update.txt", 
        f"Change Request: {change_description}", 
        f"Fix for {ticket_id}"
    )

    pr = github.create_pull_request(repo, branch_name, pr_title, pr_body)
    if pr:
        return f"PR Created: {pr.html_url}"
    return "PR creation failed."

if __name__ == "__main__":
    mcp.run()
