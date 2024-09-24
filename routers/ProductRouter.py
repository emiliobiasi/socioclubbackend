from fastapi import APIRouter
from starlette.responses import JSONResponse
from services.ProductService import ProductService
from models.products.CreateProduct import CreateProduct
from fastapi import Request

router = APIRouter()

@router.get('/product')
async def get_products():
    try:
        products = ProductService.get_products()
        return JSONResponse(content={'products': [product.dict() for product in products]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)
    
@router.get('/getProductsByClubId/{club_id}')
async def get_products_by_club_id(club_id: str):
    try:
        products = ProductService.get_products_by_club_id(club_id=club_id)
        return JSONResponse(content={'products': [product.dict() for product in products]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)
    
@router.post('/buyProduct')
async def buy_product(request: Request):
    try:

        data = await request.json()

        ProductService.buy_product(client_id=data['client_id'], product_id=data['product_id'])

        return JSONResponse(content={'message': 'Compra realizada com sucesso !'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao comprar produto: {str(e)}'}, status_code=500)
    
@router.get('/getBoughtProductsByClientId/{client_id}')
async def get_bought_products_by_client_id(client_id: str):
    try:
        products = ProductService.get_bought_products_by_client_id(client_id=client_id)

        return JSONResponse(content={'products': [product.dict() for product in products]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao retornar produtos: {str(e)}'}, status_code=500)
    
@router.post('/createProduct')
async def create_product(new_product: CreateProduct):
    try:
        ProductService.create_product(new_product=new_product)

        return JSONResponse(content={'message': 'Produto criado com sucesso!'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao criar produto: {str(e)}'}, status_code=500)
