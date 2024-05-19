from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from services.GameService import GameService


router = APIRouter()


@router.get('/games')
async def get_games():
    try:
        games = GameService.get_games()
        return JSONResponse(content={'games': [game.dict() for game in games]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter games: {str(e)}"}, status_code=500)


@router.get("/getGameByClubId/{id}")
async def find_game_by_id(id: int):
    try:
        game = GameService.find_by_id(id)
        if game:
            return JSONResponse(content={'game': game.dict()}, status_code=200)
        else:
            return JSONResponse(content={'message': 'Game não encontrado'}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar game: {str(e)}")