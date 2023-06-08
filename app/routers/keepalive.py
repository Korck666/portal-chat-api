# routers/keepalive.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import auth
from services.auth import authenticate_api_key
from services.keepalive import KeepAlive

router = APIRouter()


@router.get("/keepalive", dependencies=[Depends(authenticate_api_key)])
def keepalive() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = auth.TokenData(scopes=["keepalive"])
    # Return the response
    return KeepAlive.keepalive(auth_token)
