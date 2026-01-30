from github import Github
import time

class GithubHandler:
    def __init__(self, token):
        self.g = Github(token)
        self.user = self.g.get_user()

    def verify_access(self, repo_name):
        try:
            repo = self.g.get_repo(repo_name)
            print(f"Successfully accessed repo: {repo.full_name}")
            return repo
        except Exception as e:
            print(f"Error accessing repo {repo_name}: {e}")
            return None

    def create_branch(self, repo, branch_name):
        try:
            sb = repo.get_branch("main") # Assuming main is the default branch
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=sb.commit.sha)
            print(f"Branch {branch_name} created.")
            return True
        except Exception as e:
            print(f"Error creating branch {branch_name}: {e}")
            return False

    def create_file_update(self, repo, branch_name, file_path, content, message):
         try:
            # Check if file exists to update, else create
            try:
                contents = repo.get_contents(file_path, ref=branch_name)
                repo.update_file(contents.path, message, content, contents.sha, branch=branch_name)
                print(f"File {file_path} updated.")
            except:
                repo.create_file(file_path, message, content, branch=branch_name)
                print(f"File {file_path} created.")
            return True
         except Exception as e:
             print(f"Error updating/creating file {file_path}: {e}")
             return False

    def create_pull_request(self, repo, branch_name, title, body):
        try:
            pr = repo.create_pull(title=title, body=body, head=branch_name, base="main")
            print(f"Pull Request created: {pr.html_url}")
            return pr
        except Exception as e:
            print(f"Error creating PR: {e}")
            return None

    def check_workflow_status(self, repo, pr_number):
        print(f"Checking workflow status for PR #{pr_number}...")
        # Get the PR object
        pr = repo.get_pull(pr_number)
        head_sha = pr.head.sha
        
        # Give it a moment for workflows to trigger
        time.sleep(10)
        
        # Get check runs for the commit
        runs = repo.get_check_runs(head_sha)
        
        results = []
        for run in runs:
            results.append(f"{run.name}: {run.status} - {run.conclusion}")
            
        return "\n".join(results) if results else "No check runs found."
