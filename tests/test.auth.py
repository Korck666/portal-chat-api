import pytest

from app.services.auth import Authenticator
from fastapi import HTTPException


def test_authenticate_api_key():
    api_key = Authenticator(auth_type="api_key")

    # Test with valid credentials
    with pytest.raises(HTTPException):
        key = api_key.authenticate_api_key()
        assert key == "api_key"

    # Test with invalid credentials
    with pytest.raises(HTTPException):
        key = api_key.authenticate_api_key()
        assert key == "invalid_api_key"


def test_authenticate_user():
    oauth2 = Authenticator(auth_type="oauth2")

    # Test with valid credentials
    # 'invalid_username', 'invalid_password')
    user_data = oauth2.authenticate_user()

    # Test with invalid credentials
    with pytest.raises(HTTPException):
        # 'invalid_username', 'invalid_password')
        user_data = oauth2.authenticate_user()
