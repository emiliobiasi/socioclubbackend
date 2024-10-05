from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from services.StripeService import StripeService

router = APIRouter()

@router.post('/account')
async def create_account():
    try:
        account = StripeService.create_account()
        return JSONResponse(content={'account': account.id}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao criar a conta: {str(e)}"}, status_code=500)

@router.post('/account_link')
async def create_account_link(account: dict):
    try:
        connected_account_id = account.get('account')
        if not connected_account_id:
            raise HTTPException(status_code=400, detail="Account ID is required")

        account_link = StripeService.create_account_link(connected_account_id)
        return JSONResponse(content={'url': account_link.url}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao criar o link da conta: {str(e)}"}, status_code=500)
    
@router.post('/account/{account_id}')
async def update_account(account_id: str):
    try:
        connected_account = StripeService.update_account(account_id)
        return JSONResponse(content={'account': connected_account.id}, status_code=200)
    except Exception as e:
        print(f'An error occurred when calling the Stripe API to update an account: {e}')
        return JSONResponse(content={"message": f"Erro ao atualizar a conta: {str(e)}"}, status_code=500)

@router.post('/create_product')
async def create_product(product: dict):
    try:
        name = product.get('name')
        price = product.get('price')
        currency = product.get('currency', 'usd')
        interval = product.get('interval', None)

        if not name:
            raise HTTPException(status_code=400, detail="Product name is required")
        if price is None:
            raise HTTPException(status_code=400, detail="Product price is required")

        created_product = StripeService.create_product_with_price(
            name=name,
            price=price,
            currency=currency,
            interval=interval
        )

        return JSONResponse(content={'price_id': created_product['price'].id}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao criar o produto: {str(e)}"}, status_code=500)