# routers/healtcheck.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.token_data import TokenData
from services.auth import Authenticator
from services.healthcheck import HealthCheck

router = APIRouter()

auth = Authenticator("api_key")


@router.get("/healthcheck", dependencies=[Depends(auth.auth_header_dependency)])
async def healthcheck() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = TokenData(scopes=["healthcheck"])
    try:
        checks = await HealthCheck.healthcheck(auth_token)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

    # Return the response
    return JSONResponse(status_code=200, content={"message": checks})
