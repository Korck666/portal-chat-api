# routers/chat.py
from fastapi import APIRouter
from utils import config
from models.ChatInput import ChatInput
from models.ChatOutput import ChatOutput
from services import openai

router = APIRouter()

# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput)
def chat_endpoint(chat_input: ChatInput):
    # Return the response
    return ChatOutput(response=openai.chat(config.CHAT_MODEL, chat_prep, chat_input.message))
