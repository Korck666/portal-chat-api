# routers/healtcheck.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import auth
from services.auth import authenticate_api_key
from services.healthcheck import HealthCheck

router = APIRouter()


@router.get("/healthcheck", dependencies=[Depends(authenticate_api_key)])
def healthcheck() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = auth.TokenData(scopes=["healthcheck"])
    # Return the response
    return HealthCheck.healthcheck(auth_token)
