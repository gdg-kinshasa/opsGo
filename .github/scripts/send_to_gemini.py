import os
import json
import requests

TRIVY_FILE = "trivy-results.json"
OUTPUT_FILE = "gemini-response.txt"
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

if not API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY environment variable is not set.")

# Append API key as URL query parameter
url = f"{GEMINI_ENDPOINT}?key={API_KEY}"

# Load Trivy scan results
with open(TRIVY_FILE, "r") as f:
    trivy_data = json.load(f)

# Build the prompt
prompt_text = f"""
The following is a vulnerability scan of a Docker image using Trivy.
Please analyze the issues and suggest secure fixes for each finding.

```json
{json.dumps(trivy_data, indent=2)}
```
"""

# Prepare the request payload
payload = {
    "contents": [
        {
            "parts": [{"text": prompt_text}]
        }
    ]
}

# Make the POST request
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    json=payload
)

# Handle the response
if response.status_code == 200:
    try:
        ai_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        with open(OUTPUT_FILE, "w") as out:
            out.write(ai_reply)
        print("✅ AI suggestions saved to gemini-response.txt")
    except (KeyError, IndexError):
        print("⚠️ Received unexpected response format:")
        print(response.json())
        exit(1)
else:
    print("❌ Error from Gemini:", response.status_code)
    print(response.text)
    exit(1)
