import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINEAR_API_URL = "https://api.linear.app/graphql"

def query_linear_api(query):
    
    access_token = os.getenv("LINEAR_TOKEN")
    if not access_token:
        raise ValueError("Linear token not found.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "query": query
    }

    response = requests.post(LINEAR_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code: {response.status_code}")

query = "{ issues { nodes { id title } } }"

try:
    result = query_linear_api(query)
    print(result)
except Exception as e:
    print(f"An error occurred: {str(e)}")