# routers/chat.py
from fastapi import APIRouter, Depends
from services.auth import authenticate_api_key
from utils import config
from models.chat_input import ChatInput
from models.chat_output import ChatOutput
from services import openai

router = APIRouter()

# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput, dependencies=[Depends(authenticate_api_key)])
def chat_endpoint(chat_input: ChatInput):
    # we may do some preprocessing here
    # Return the response
    return ChatOutput(response=openai.chat(config.CHAT_MODEL, chat_prep, chat_input.message))
