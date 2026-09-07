from dotenv import load_dotenv
load_dotenv()

from groq import Groq

client = Groq()


def get_client():
    return client


def ask_question(context, question):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Answer ONLY using this context. If the answer isn't in the context, say so.\n\nContext:\n{context}\n\nQuestion: {question}"
        }]
    )
    return response.choices[0].message.content
