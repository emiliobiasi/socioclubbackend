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
