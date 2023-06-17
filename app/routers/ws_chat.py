from fastapi import APIRouter, Depends, WebSocket
from services.auth import Authenticator
from services.openai import OpenAI

# import openai
router = APIRouter()
openai = OpenAI()

@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        report = []
        # Wait for the client to send a message
        chat_input = await websocket.receive_text()
        # Send the message to the ChatGPT model and get a response
        for response in openai.chat("gpt-3.5-turbo", "You are a helpful assistant.", chat_input):#, stream=True):
            # Send the response back to the client over the WebSocket
            report.append(response.choices[0].text)
            result = "".join(report).strip()
            result = result.replace("\n", "")        
            await websocket.send_text(result)
