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
