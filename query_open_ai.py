import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GPT_MODEL = "gpt-3.5-turbo"
MAX_GPT_TOKENS = 150

def query_openai(prompt, model=GPT_MODEL, max_tokens=MAX_GPT_TOKENS):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None