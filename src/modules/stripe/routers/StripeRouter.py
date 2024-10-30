from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse
from models.stripe.create_product_stripe import CreateProductStripe
from models.stripe.vinculate import Vinculate
from src.modules.stripe.services.StripeService import StripeService

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
        StripeService.vinculate(
            socioclub_id=temp['socioclub_id'],
            stripe_id=temp['stripe_id'],
            price_id=temp['price_id'],
            is_product=temp['is_product']
        )
        return JSONResponse(content={"message": "Produto vinculado com sucesso."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao vincular: {str(e)}"}, status_code=500)
    





# NOVAS ROTAS PARA ASSINATURAS

@router.post('/create_customer')
async def create_customer(request: dict):
    try:
        email = request.get('email')
        name = request.get('name')
        stripe_account_id = request.get('stripe_account_id')

        if not email:
            raise HTTPException(status_code=400, detail="Email é obrigatório")

        customer = StripeService.create_customer(
            email=email,
            name=name,
            stripe_account=stripe_account_id
        )
        return {'customer_id': customer.id}
    except Exception as e:
        print(f"Erro ao criar o cliente: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar o cliente: {str(e)}")

# Nova rota para criar produto de assinatura
@router.post('/create_subscription_product')
async def create_subscription_product(request: dict):
    try:
        name = request.get('name')
        price = request.get('price')
        currency = request.get('currency', 'usd')
        interval = request.get('interval', 'month')
        stripe_account_id = request.get('stripe_account_id')

        if not name or not price or not interval:
            raise HTTPException(status_code=400, detail="Nome, preço e intervalo são obrigatórios")

        created_price = StripeService.create_subscription_product(
            name=name,
            price=price,
            currency=currency,
            interval=interval,
            stripe_account=stripe_account_id
        )

        return {
            'price_id': created_price['id'],
            'product_id': created_price['product']
        }
    except Exception as e:
        print(f"Erro ao criar o produto de assinatura: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar o produto de assinatura: {str(e)}")

@router.post('/create_checkout_session_subscription')
async def create_checkout_session_subscription(request: dict):
    try:
        price_id = request.get('price_id')
        success_url = request.get('success_url')
        cancel_url = request.get('cancel_url')
        stripe_account_id = request.get('stripe_account_id')

        if not price_id or not success_url or not cancel_url:
            raise HTTPException(status_code=400, detail="Price ID, Success URL e Cancel URL são obrigatórios")

        session = StripeService.create_checkout_session_for_subscription(
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url,
            stripe_account=stripe_account_id
        )
        return {'checkout_url': session.url}
    except Exception as e:
        print(f"Erro ao criar a sessão de checkout: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar a sessão de checkout: {str(e)}")

@router.get('/retrieve_checkout_session')
async def retrieve_checkout_session(session_id: str, stripe_account_id: str = None):
    try:
        session = StripeService.retrieve_checkout_session(
            session_id=session_id,
            stripe_account=stripe_account_id
        )
        return session
    except Exception as e:
        print(f"Erro ao recuperar a sessão de checkout: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar a sessão de checkout: {str(e)}")

@router.get('/retrieve_subscription')
async def retrieve_subscription(subscription_id: str, stripe_account_id: str = None):
    try:
        subscription = StripeService.retrieve_subscription(
            subscription_id=subscription_id,
            stripe_account=stripe_account_id
        )
        return subscription
    except Exception as e:
        print(f"Erro ao recuperar a assinatura: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar a assinatura: {str(e)}")