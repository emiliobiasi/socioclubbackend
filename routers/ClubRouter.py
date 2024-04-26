from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
#from services.ClientService import ClientService

from models.Club import Club


router = APIRouter()

@router.get('/clubs')
async def get_clubs():
    try:
        clubs = 0
        return JSONResponse(content={'clubs': [club.dict() for club in clubs]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)