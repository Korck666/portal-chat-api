# routers/keepalive.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.authenticator import Authenticator
from services.keepalive import KeepAlive
from models.token_data import TokenData

router = APIRouter()

auth = Authenticator("api_key")


@router.get("/keepalive", dependencies=[Depends(auth.auth_header_dependency)])
def keepalive() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = TokenData(scopes=["keepalive"])
    # Return the response
    return KeepAlive.keepalive(auth_token)
