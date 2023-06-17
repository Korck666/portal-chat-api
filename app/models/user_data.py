# Define a Pydantic data model for the user data
import re
from typing import Any, Optional

import pydantic
from pydantic import BaseModel, EmailStr, Field


class UserData(BaseModel):
    # EmailStr is used to validate email format
    email: EmailStr = Field(
        None, description="The user's email address", example="jdoe@example.com")
    # password rules:
    # accepts:
    # - only letters, space, special characters and numbers
    # not allowed:
    # - any characters to be repeated in sequence more than 2 times
    # - more than 1 pair of the same character
    # - same character total count be more than 3
    # required:
    # - password must be at least 8 characters long and at most 12 characters long
    # - password must contain at least one number
    # - password must contain at least one special character
    # - password must contain at least one uppercase letter
    # - min length of 8 characters and max length of 12 characters
    password_regex = r"^(?!.*(.)(\1{2,}))(?!.*(.)(.*\3){1})(?!.*(.).*\4.*\4)(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()_+={}\[\]:;\"'<>,.?/\\|~-]).{8,12}$"
    password: str = Field(
        None, description="The user's password", example="P@ssw0rd!", regex=password_regex, min_length=8, max_length=12)
    # accepts only letters, space, _, and numbers
    # max length of 12 characters
    nickname: str = Field(
        None, description="The user's nickname", example="jedi", regex=r"^[a-zA-Z0-9_ ]+$", max_length=12)
    is_active: bool = Field(
        True, description="Whether the user is active", example=True)
    is_superuser: bool = Field(
        False, description="Whether the user is a superuser", example=False)
    # ------------------------------------------------------
    # private fields
    # ------------------------------------------------------
    full_name: Optional[str] = Field(
        None, description="The user's name", example="Jane Doe", regex=r"^[\p{L} ]+$", max_length=64)
    phone_number: Optional[str] = Field(
        None, description="The user's phone number", example="+1-541-754-3010", regex=r"^\+?[0-9- ]+$", max_length=16)
    address: Optional[str] = Field(None, description="The user's address",
                                   example="123 Main Street", regex=r"^[\p{L} ]+$", max_length=64)
    city: Optional[str] = Field(None, description="The user's city",
                                example="San Francisco", regex=r"^[\p{L} ]+$", max_length=64)
    state: Optional[str] = Field(
        None, description="The user's state", example="CA", regex=r"^[\p{L} ]+$", max_length=2)
    zip_code: Optional[str] = Field(
        None, description="The user's zip code", example="94107", regex=r"^\d{5}$", max_length=5)
    country: Optional[str] = Field(
        None, description="The user's country", example="US", regex=r"^[A-Z]{2}$", max_length=2)
    date_of_birth: Optional[str] = Field(
        None, description="The user's date of birth", example="1990-01-01", regex=r"^\d{4}-\d{2}-\d{2}$", max_length=10)
