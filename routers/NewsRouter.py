from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
from services.NewsService import NewsService

from models.News import News


router = APIRouter()

@router.get('/news')
async def get_news():
    try:
        news = NewsService.get_news()
        return JSONResponse(content={'news': [new.dict() for new in news]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)