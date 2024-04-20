from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
from services.AuthService import AuthService

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    
    access_data = AuthService.login(email=data["email"], password=data["password"])
    
    return JSONResponse(
        content=access_data,
        status_code=status.HTTP_200_OK
    )
