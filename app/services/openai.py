# services/openai.py
import openai
from utils import config

openai.api_key = config.OPENAI_API_KEY
openai.organization = config.OPENAI_ORGANIZATION


def chat(chat_model: str, chat_prep: str, chat_message: str) -> str:
    # Call OpenAI API
    openai_response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": chat_prep},
            {"role": "user", "content": chat_message},
        ]
    )
    # type: ignore
    response_message = openai_response["choices"][0]["message"]["content"]
    return response_message
