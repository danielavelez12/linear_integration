DECIDE_ACTION = {
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

CLASSIFY = {
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