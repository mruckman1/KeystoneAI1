import os
from github import Github
import base64
import mimetypes
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables explicitly from .env file
dotenv_path = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/.env'
load_dotenv(dotenv_path=dotenv_path)

# Load and verify GITHUB_TOKEN
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if GITHUB_TOKEN:
    print(f"Token loaded: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")  # Print partial token for confirmation
else:
    print("Token not loaded correctly. Check .env file path and format.")

# Initialize GitHub client
try:
    g = Github(GITHUB_TOKEN)
    user = g.get_user()  # Test the connection
    print("Authenticated as:", user.login)
except Exception as e:
    print("Authentication failed:", e)

# Define patterns to exclude from processing
EXCLUDE_PATTERNS = {
    "ISSUE_TEMPLATE", "PULL_REQUEST_TEMPLATE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", ".github",
    "docs", "LICENSE", "README.md", "CHANGELOG.md", "templates", "example", "examples",
    "test", "tests", "demo", "demos", "Makefile", "Dockerfile", "requirements.txt", "Pipfile",
    "Pipfile.lock", "package.json", "package-lock.json", "yarn.lock", ".env", ".gitignore",
    "dist", "build", "out", "node_modules", "ci", ".circleci", ".travis.yml", ".vscode", ".idea", "logs"
}

def is_excluded(name):
    name_lower = name.lower()
    for pattern in EXCLUDE_PATTERNS:
        pattern_lower = pattern.lower()
        if name_lower == pattern_lower or pattern_lower in name_lower:
            return True
    return False

def is_binary_string(bytes_data):
    text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    if not bytes_data:
        return False
    if b'\0' in bytes_data:
        return True
    nontext = bytes([b for b in bytes_data if b not in text_characters])
    return bool(nontext)

def process_file_content(repo, file_content, path):
    decoded_content = base64.b64decode(file_content.content)
    if is_binary_string(decoded_content):
        return ""
    try:
        decoded_content = decoded_content.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        return ""
    file_text = f"\n## {path}\n\n```\n{decoded_content}\n```\n"
    return file_text

def process_repo_contents(repo, contents, base_path="", indent_level=0):
    repo_text = ""
    structure_text = ""
    indent = "│   " * indent_level
    for i, content_file in enumerate(contents):
        if is_excluded(content_file.name):
            continue
        connector = "└── " if i == len(contents) - 1 else "├── "
        full_path = os.path.join(base_path, content_file.name)
        
        if content_file.type == "dir":
            structure_text += f"{indent}{connector}{content_file.name}/\n"
            try:
                sub_contents = repo.get_contents(content_file.path)
            except Exception as e:
                print(f"Failed to get contents of directory {content_file.path}: {e}")
                continue
            dir_text, dir_structure = process_repo_contents(repo, sub_contents, full_path, indent_level + 1)
            repo_text += dir_text
            structure_text += dir_structure
        else:
            structure_text += f"{indent}{connector}{content_file.name}\n"
            mime_type, _ = mimetypes.guess_type(content_file.path)
            if mime_type and mime_type.startswith("text"):
                repo_text += process_file_content(repo, content_file, full_path)
            else:
                try:
                    file_content = repo.get_contents(content_file.path)
                    decoded_content = base64.b64decode(file_content.content)
                    if not is_binary_string(decoded_content):
                        repo_text += process_file_content(repo, file_content, full_path)
                except Exception as e:
                    print(f"Failed to process file {content_file.path}: {e}")
                    continue
    return repo_text, structure_text

def fetch_recent_issues(repo):
    """
    Fetch issues from the past 3 months with additional contextual information.
    """
    issues_text = "\n## Recent Issues (Past 3 Months)\n\n"
    since_date = datetime.now(timezone.utc) - timedelta(days=90)
    
    try:
        issues = repo.get_issues(state='all', since=since_date)
        for issue in issues:
            if issue.created_at >= since_date:
                issues_text += f"### Issue #{issue.number}: {issue.title}\n"
                issues_text += f"- **Created at**: {issue.created_at}\n"
                issues_text += f"- **State**: {issue.state}\n"
                issues_text += f"- **User**: {issue.user.login}\n"
                issues_text += f"- **Labels**: {[label.name for label in issue.labels]}\n"
                
                # Assignees
                assignees = [assignee.login for assignee in issue.assignees]
                issues_text += f"- **Assignees**: {assignees if assignees else 'None'}\n"
                
                # Milestone
                issues_text += f"- **Milestone**: {issue.milestone.title if issue.milestone else 'None'}\n"
                
                # Closed date
                issues_text += f"- **Closed at**: {issue.closed_at if issue.closed_at else 'Still open'}\n"
                
                # Last Updated
                issues_text += f"- **Last Updated**: {issue.updated_at}\n"

                # Attempt to find potential PR links in the issue body or comments
                issues_text += "- **Potential Pull Request Links**:\n"
                
                # Check in issue body
                if issue.body:
                    pr_links = [line for line in issue.body.splitlines() if "pull" in line or "PR" in line]
                    for link in pr_links:
                        issues_text += f"  - {link}\n"
                
                # Check in comments for potential PR links
                comments = issue.get_comments()
                if comments.totalCount > 0:
                    issues_text += "- **Comments**:\n"
                    for comment in comments:
                        issues_text += f"  - {comment.user.login} ({comment.created_at}): {comment.body}\n"
                        comment_pr_links = [line for line in comment.body.splitlines() if "pull" in line or "PR" in line]
                        for link in comment_pr_links:
                            issues_text += f"    - Potential PR Link: {link}\n"

                # Issue body
                issues_text += f"- **Body**:\n{issue.body}\n\n"

    except Exception as e:
        print(f"Failed to fetch issues: {e}")
        issues_text += "Failed to retrieve issues data.\n"
    
    return issues_text

def repo_to_text(github_url, output_dir):
    """
    Convert a GitHub repository to a structured text file, including recent issues.
    """
    g = Github(GITHUB_TOKEN)
    repo_name = github_url.replace("https://github.com/", "").split('/tree/')[0]
    
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        print(f"Failed to access repository {repo_name}: {e}")
        return

    try:
        contents = repo.get_contents("")
    except Exception as e:
        print(f"Failed to get contents of repository {repo_name}: {e}")
        return

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
    safe_repo_name = repo_name.replace('/', '_')
    output_file = os.path.join(output_dir, f"{safe_repo_name}_{timestamp}.txt")

    repo_text = f"# Repository: {repo_name}\n"
    repo_text += "\n## Repository Structure\n\n"
    contents_text, structure_text = process_repo_contents(repo, contents)
    repo_text += f"```\n{structure_text}\n```\n"
    repo_text += contents_text
    
    # Append recent issues to the text
    repo_text += fetch_recent_issues(repo)

    try:
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(repo_text)
        print(f"Repository contents and issues have been written to {output_file}")
    except Exception as e:
        print(f"Failed to write to file {output_file}: {e}")

# Example usage
if __name__ == "__main__":
    github_url = "https://github.com/openai/swarm"  # Replace with the target GitHub repo URL
    output_dir = "/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/data"  # Set as directory path
    repo_to_text(github_url, output_dir)
