import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINEAR_API_URL = "https://api.linear.app/graphql"

def get_linear_headers():
    access_token = os.getenv("LINEAR_TOKEN")
    if not access_token:
        raise ValueError("Linear token not found.")
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

def query_linear_api(query, variables=None):
    headers = get_linear_headers()
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(LINEAR_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code: {response.status_code}")

def get_linear_tasks():
    query = """
    query {
        issues {
            nodes {
                id
                title
                description
            }
        }
    }
    """
    result = query_linear_api(query)
    return result['data']['issues']['nodes']