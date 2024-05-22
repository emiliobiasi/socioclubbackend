from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
from services.ClubService import ClubService

from models.Club import Club


router = APIRouter()

@router.get('/clubs')
async def get_clubs():
    try:
        clubs = ClubService.get_clubs()
        return JSONResponse(content={'clubs': [club.dict() for club in clubs]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)
    
@router.get("/findClubById/{id}")
async def find_client_by_id(id: int):
    try:
        club = ClubService.find_by_id(id)
        if club:
            return JSONResponse(content={'club': club.dict()}, status_code=200)
        else:
            return JSONResponse(content={'message': 'Clube não encontrado'}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar clube: {str(e)}")
    
@router.get('/getFollowingClubs/{client_id}')
async def get_following_club(client_id: str):
    try:

        clubs = ClubService.get_following_clubs(client_id)
        
        return JSONResponse(content={'clubs': clubs}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao retornar clubes: {str(e)}")