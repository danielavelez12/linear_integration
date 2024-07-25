import json

def get_decide_action_message(new_task, existing_tasks):
    return f"""
        New task:
        Title: {new_task.title}
        Description: {new_task.description}

        Existing tasks:
        {json.dumps(existing_tasks, indent=2)}

        Based on the new task and the list of existing tasks, determine if we should:
        1. Add this as a new task
        2. Add a comment to an existing task
        """