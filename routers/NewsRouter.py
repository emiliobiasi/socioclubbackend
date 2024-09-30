from fastapi import APIRouter
from starlette.responses import JSONResponse
from services.NewsService import NewsService
from models.news.CreateNews import CreateNews

router = APIRouter()

@router.get('/news')
async def get_news():
    try:
        news = NewsService.get_news()
        return JSONResponse(content={'news': [new.dict() for new in news]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter noticias: {str(e)}"}, status_code=500)
    
@router.get('/getNewsByClubId/{club_id}')
async def get_news(club_id: str):
    try:
        news = NewsService.get_news_by_club_id(club_id=club_id)
        return JSONResponse(content={'news': [new.dict() for new in news]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter noticias: {str(e)}"}, status_code=500)

@router.post('/createNews')
async def create_news(new_news: CreateNews):
    try:
        data = NewsService.create_news(new_news=new_news)
        return JSONResponse(content={'message': 'noticia criada com sucesso', 'data': data.dict()}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao criar noticia: {str(e)}"}, status_code=500)
    
@router.delete('/deleteNew/{new_id}')
async def delete_new(new_id: str):
    try:
        data = NewsService.delete_new(new_id=new_id)
        return JSONResponse(content={'message': 'noticia deletada com sucesso'}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao deletar noticia: {str(e)}"}, status_code=500)