
from query_open_ai import query_openai


prompt = """
Here is a chat transcript. Output nothing else but a JSON object in this sample format:

{
    feature_request: {
        present: true,
        content: "Example feature request"
    },
    bug_report: {
        present: true,
        content: "Example bug report"
    },
}

Chat transcript:
"""

def main(chat_transcript):
    print(query_openai(prompt + "\n" + chat_transcript))

if __name__ == "__main__":
    main("User: I can't log in. Support: We'll look into it!")