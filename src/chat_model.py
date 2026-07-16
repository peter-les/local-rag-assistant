#chat_model.py
import ollama
from config import LLM_MODEL

def ask_llm_stream(prompt: str):
    # Voláme ollama.chat so stream=True
    response_stream = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.0
        },
        stream=True # <--- Zapíname streaming
    )
    return response_stream