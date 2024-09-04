from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
from services.ClubCategoryService import ClubCategoryService

from models.clubs.Club import Club


router = APIRouter()

@router.get('/clubCategories')
async def get_club_categoires():
    try:
        clubs = ClubCategoryService.get_club_categories()
        return JSONResponse(content={'clubCategories': [club.dict() for club in clubs]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)
    
