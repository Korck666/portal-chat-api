import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.chat_input import ChatInput

client = TestClient(app)

def test_chat_endpoint():
    # Test with valid input
    response = client.post(
        "/chat",
        json=ChatInput(message="test message").dict()
    )
    assert response.status_code == 200
    assert "response" in response.json()

    # Test with invalid input
    response = client.post(
        "/chat",
        json={}
    )
    assert response.status_code == 422  # HTTP status code for Unprocessable Entity
