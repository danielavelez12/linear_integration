import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def query_openai(messages, tools=None, tool_choice="auto"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4", 
        "messages": messages,
        "tools": tools,
        "tool_choice": tool_choice
    }
    
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    return response.json()
