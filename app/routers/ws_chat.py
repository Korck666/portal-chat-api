from time import sleep
from fastapi import APIRouter, Depends, WebSocket
from services.auth import Authenticator
from services.openai import OpenAI
from services.logger import Logger

logger = Logger()
# import openai
router = APIRouter()
openai = OpenAI()


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        chunks = []
        messages = []
        # Wait for the client to send a message
        chat_input = await websocket.receive_text()
        # Send the message to the ChatGPT model and get a response
        response = openai.chat(
            "gpt-3.5-turbo", "You are a helpful assistant.", chat_input, stream=True)

        # Iterate over the response and send each message
        for chunk in response:
            # get the message from the response
            # chunks.append(chunk["choices"][0]["delta"])
            messages.append(chunk["choices"][0]["delta"].get("content", ""))
            await websocket.send_text(messages[-1])
            sleep(0.05)

