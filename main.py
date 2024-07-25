import json
from dotenv import load_dotenv
from add_comment_to_task import add_comment_to_task
from create_linear_task import create_linear_task
from fetch_linear_tasks import get_linear_tasks
from query_open_ai import query_openai

load_dotenv()

def handle_new_task(new_task):
    existing_tasks = get_linear_tasks()

    messages = [
        {"role": "user", "content": f"""
        New task:
        Title: {new_task.title}
        Description: {new_task.description}

        Existing tasks:
        {json.dumps(existing_tasks, indent=2)}

        Based on the new task and the list of existing tasks, determine if we should:
        1. Add this as a new task
        2. Add a comment to an existing task
        """}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "decide_action",
                "description": "Decide whether to create a new task or add a comment to an existing one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["new_task", "add_comment"]
                        },
                        "reason": {
                            "type": "string",
                            "description": "Brief explanation of the decision"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "ID of the existing task if adding a comment, otherwise null"
                        }
                    },
                    "required": ["action", "reason"]
                }
            }
        }
    ]

    response = query_openai(messages, tools=tools)

    try:
        tool_call = response['choices'][0]['message'].get('tool_calls', [])
        if tool_call:
            decision = json.loads(tool_call[0]['function']['arguments'])

            if decision["action"] == "new_task":
                result = create_linear_task(new_task.title, new_task.description, "Engineering")
                print(f"New task created: {result['data']['issueCreate']['issue']['id']}")
                print(f"Reason: {decision['reason']}")

            elif decision["action"] == "add_comment":
                comment = f"Related to: {new_task.title}\n{new_task.description}"
                result = add_comment_to_task(decision["task_id"], comment)
                print(f"Comment added to task {decision['task_id']}")
                print(f"Reason: {decision['reason']}")

            else:
                print(f"Unknown action: {decision['action']}")
        else:
            print("No tool call in the response")

    except json.JSONDecodeError:
        print("Failed to parse JSON response from OpenAI")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main(chat_transcript):
    messages = [
        {"role": "user", "content": chat_transcript}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "classify_transcript",
                "description": "Classify the chat transcript as a bug report, feature request, or neither",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["bug_report", "feature_request", "none"]
                        },
                        "content": {
                            "type": "string",
                            "description": "Summary of the bug report or feature request"
                        }
                    },
                    "required": ["type"]
                }
            }
        }
    ]

    response = query_openai(messages, tools=tools)
    
    try:
        tool_call = response['choices'][0]['message'].get('tool_calls', [])
        if tool_call:
            classification = json.loads(tool_call[0]['function']['arguments'])
            
            if classification["type"] == "feature_request":
                new_task = Task(
                    title="Feature Request: " + classification["content"][:50] + "...",
                    description=classification["content"]
                )
                handle_new_task(new_task)
            elif classification["type"] == "bug_report":
                new_task = Task(
                    title="Bug Report: " + classification["content"][:50] + "...",
                    description=classification["content"]
                )
                handle_new_task(new_task)
            else:
                print("No actionable item found in the chat transcript.")
        else:
            print("No tool call in the response")
        
    except json.JSONDecodeError:
        print("Failed to parse JSON response from OpenAI")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description

if __name__ == "__main__":
    main("User: I can't log in. Support: We'll look into it!")