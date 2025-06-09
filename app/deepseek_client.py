import requests
import os
API_KEY = "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"  # 🔐 Replace this!

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

def query_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(ENDPOINT, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
