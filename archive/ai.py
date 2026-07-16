from ollama import chat

def ask_ai(question):
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]