import json
from dotenv import load_dotenv
from functions import DECIDE_ACTION, CLASSIFY
from messages import get_decide_action_message
from task import Task
from add_comment_to_task import add_comment_to_task
from create_linear_task import create_linear_task
from fetch_linear_tasks import get_linear_tasks
from query_open_ai import query_openai

load_dotenv()

MAX_TITLE_LENGTH = 50
DEFAULT_TEAM = "Engineering"

def handle_new_task(new_task):
    existing_tasks = get_linear_tasks()

    messages = [
        {"role": "user", "content": get_decide_action_message(new_task, existing_tasks)}
    ]

    tools = [
        {
            "type": "function",
            "function": DECIDE_ACTION
        }
    ]

    response = query_openai(messages, tools=tools)

    try:
        tool_call = response['choices'][0]['message'].get('tool_calls', [])
        if tool_call:
            decision = json.loads(tool_call[0]['function']['arguments'])

            if decision["action"] == "new_task":
                result = create_linear_task(new_task.title, new_task.description, DEFAULT_TEAM)
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
            "function": CLASSIFY
        }
    ]

    response = query_openai(messages, tools=tools)
    
    try:
        tool_call = response['choices'][0]['message'].get('tool_calls', [])
        if tool_call:
            classification = json.loads(tool_call[0]['function']['arguments'])
            
            if classification["type"] == "feature_request":
                new_task = Task(
                    title=f"Feature Request: {classification['content'][:MAX_TITLE_LENGTH]}...",
                    description=classification["content"]
                )
                handle_new_task(new_task)
            elif classification["type"] == "bug_report":
                new_task = Task(
                    title=f"Bug Report: {classification['content'][:MAX_TITLE_LENGTH]}...",
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

if __name__ == "__main__":
    main("User: I can't log in. Support: We'll look into it!")