from fastapi import APIRouter
from starlette.responses import JSONResponse
from services.ProductService import ProductService

from models.News import News


router = APIRouter()

@router.get('/product')
async def get_news():
    try:
        products = ProductService.get_products()
        return JSONResponse(content={'products': [product.dict() for product in products]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)
    
@router.get('/getProductsByClubId/{club_id}')
async def get_news(club_id: str):
    try:
        products = ProductService.get_products_by_club_id(club_id=club_id)
        return JSONResponse(content={'products': [product.dict() for product in products]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)