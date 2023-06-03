# services/openai.py
from typing import Any, Generator
import openai
from utils import config

openai.api_key = config.OPENAI_API_KEY
openai.organization = config.OPENAI_ORGANIZATION


def chat(chat_model: str, chat_prep: str, chat_message: str) -> str:
    # Call OpenAI API
    openai_response: Any = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": chat_prep},
            {"role": "user", "content": chat_message},
        ]
    )

    response_message: Any = openai_response["choices"]
    response_message: Any = response_message[0]
    response_message: Any = response_message["message"]
    response_message: Any = response_message["content"]

    return response_message
