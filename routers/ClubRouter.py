from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from models.clubs.RegisterClub import RegisterClub
from models.clubs.RegisterStripeClub import RegisterStripeClub
from models.clubs.ColorSchemeClub import ColorSchemeClub
from models.clubs.LoginClub import LoginClub
from services.ClubService import ClubService

from models.clubs.Club import Club


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
            return JSONResponse(content={'club': club.to_json()}, status_code=200)
        else:
            return JSONResponse(content={'message': 'Clube não encontrado'}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar clube: {str(e)}")
    
@router.get('/getFollowingClubs/{client_id}')
async def get_following_club(client_id: str):
    try:

        clubs = ClubService.get_following_clubs(client_id)
        
        return JSONResponse(content={'clubs': [club.dict() for club in clubs]}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao retornar clubes: {str(e)}")

@router.post('/createClub')
async def create_club(club: Club):
    print("club: " + str(club))
    try:
        ClubService.create_club(club=club)
        return JSONResponse(content={'success': 'Clube criado',}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao criar clube: {e}')

@router.post('/clubLogin')
async def login(club: LoginClub):
    try:
        body = ClubService.login(club=club)
        return JSONResponse(content=body, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao realizar login: {e}')

@router.put('/updateColorScheme/{club_id}')
async def update_color_scheme(colors: ColorSchemeClub, club_id: int):
    try:
        ClubService.update_color_scheme(colors= colors, club_id= club_id)
        return JSONResponse(content={'success': 'Cores atualizadas'}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao atualizar cores: {e}')
    
@router.put('/updateStripeId')
async def update_stripe_id(teste: RegisterStripeClub):
    try:
        updated_club = ClubService.update_stripe_id(stripe_id=teste.stripe_id, club_id=teste.club_id)
        if updated_club:
            return JSONResponse(content={'success': 'Stripe ID atualizado', 'club': updated_club.to_json()}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail='Clube não encontrado')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao atualizar Stripe ID: {e}')

