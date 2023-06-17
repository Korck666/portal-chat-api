import pytest
from services.auth import Authenticator
from fastapi import HTTPException

def test_authenticate_user():
    api_key = Authenticator(auth_type="api_key")
    oauth2 = Authenticator(auth_type="oauth2")

    # Test with valid credentials
    result = oauth2.authenticate_user('valid_username', 'valid_password')
    assert result == True  # Assuming authenticate_user returns True for valid credentials

    # Test with invalid credentials
    with pytest.raises(HTTPException):
        auth.authenticate_user('invalid_username', 'invalid_password')
