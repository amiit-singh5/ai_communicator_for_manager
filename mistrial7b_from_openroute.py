# accessing Mistral7B from openroute

import requests

API_KEY = "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"
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {"Authorization": f"Bearer {API_KEY}"}
json = {
  "model": "mistralai/mistral-7b-instruct:free",
  "messages": [
    {"role":"user","content":"A developer says he needs 8 more hours. How do you respond?"}
  ],
  "max_tokens":50
}

resp = requests.post(url, headers=headers, json=json)
print(resp.json())
