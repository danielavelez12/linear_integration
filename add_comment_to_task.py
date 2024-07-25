from fetch_linear_tasks import query_linear_api

def add_comment_to_task(task_id, comment):
    mutation = """
    mutation CreateComment($issueId: String!, $body: String!) {
        commentCreate(input: {
            issueId: $issueId,
            body: $body
        }) {
            success
            comment {
                id
                body
            }
        }
    }
    """
    variables = {
        "issueId": task_id,
        "body": comment
    }
    return query_linear_api(mutation, variables)