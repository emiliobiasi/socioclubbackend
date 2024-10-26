from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse
from models.stripe.create_product_stripe import CreateProductStripe
from models.stripe.vinculate import Vinculate
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
async def create_product(request: CreateProductStripe):
    try:
        stripe_account_id = request.stripe_account_id

        print("stripe_acc: " + stripe_account_id + "   " + request.stripe_account_id)

        created_product = StripeService.create_product_with_price(
            name=request.name,
            price=request.price,
            currency=request.currency,
            interval=request.interval,
            stripe_account=stripe_account_id
        )

        return {
            'price_id': created_product['id'],
            'product_id': created_product['product']
        }
    except Exception as e:
        print(f"Erro ao criar o produto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar o produto: {str(e)}")


@router.post('/vinculate')
async def vinculate(temp: dict):
    try:

        StripeService.vinculate(socioclub_id=temp['socioclub_id'], stripe_id=temp['stripe_id'], price_id=temp['price_id'])
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao vincular: {str(e)}"}, status_code=500)