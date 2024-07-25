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

def get_team_id(team_name):
    query = """
    query GetTeamId($teamName: String!) {
        teams(filter: {name: {eq: $teamName}}) {
            nodes {
                id
                name
            }
        }
    }
    """
    variables = {"teamName": team_name}
    payload = {"query": query, "variables": variables}
    response = requests.post(LINEAR_API_URL, json=payload, headers=get_linear_headers())
    if response.status_code == 200:
        data = response.json()
        teams = data.get('data', {}).get('teams', {}).get('nodes', [])
        if teams:
            return teams[0]['id']
    raise ValueError(f"Team '{team_name}' not found.")

def create_linear_task(title, description, team_name):
    team_id = get_team_id(team_name)
    
    mutation = """
    mutation CreateIssue($title: String!, $description: String!, $teamId: String!) {
        issueCreate(input: {
            title: $title,
            description: $description,
            teamId: $teamId
        }) {
            success
            issue {
                id
                title
                url
            }
        }
    }
    """

    variables = {
        "title": title,
        "description": description,
        "teamId": team_id
    }

    payload = {
        "query": mutation,
        "variables": variables
    }

    response = requests.post(LINEAR_API_URL, json=payload, headers=get_linear_headers())
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Mutation failed with status code: {response.status_code}")

try:
    result = create_linear_task(
        title="New Task Title",
        description="This is a description of the new task.",
        team_name="Engineering"
    )
    print(result)
except Exception as e:
    print(f"An error occurred: {str(e)}")