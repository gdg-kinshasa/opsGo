import os
import json
import requests

TRIVY_FILE = "trivy-results.json"
OUTPUT_FILE = "gemini-response.txt"
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Load Trivy scan results
with open(TRIVY_FILE, "r") as f:
    trivy_data = json.load(f)

# Prepare prompt for Gemini
prompt_text = f"""
The following is a vulnerability scan of a Docker image using Trivy.
Please analyze the issues and suggest secure fixes for each finding.

```json
{json.dumps(trivy_data, indent=2)}
```
"""

# Create request payload
payload = {
    "contents": [{
        "parts": [{"text": prompt_text}]
    }]
}

# Send request to Gemini
response = requests.post(
    GEMINI_ENDPOINT,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json=payload
)

# Save response
if response.status_code == 200:
    ai_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    with open(OUTPUT_FILE, "w") as out:
        out.write(ai_reply)
    print("AI suggestions saved to gemini-response.txt")
else:
    print("Error from Gemini:", response.text)
    exit(1)
