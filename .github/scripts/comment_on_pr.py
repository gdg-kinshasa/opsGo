import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")  # e.g., bashizip/opsGo
PR_NUMBER = os.getenv("GITHUB_PR_NUMBER")
COMMENT_FILE = "gemini-response.txt"

# Load AI-generated suggestions
with open(COMMENT_FILE, "r") as f:
    comment_body = f.read()

# Prepare GitHub API request
url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

payload = {"body": f"\ud83e\udde0 **AI Suggestions from Gemini**\n\n{comment_body}"}

# Post comment to PR
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print("Successfully posted AI suggestions to the PR.")
else:
    print("Failed to post comment:", response.status_code, response.text)
    exit(1)
