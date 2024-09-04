from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.plans.RegisterPlan import RegisterPlan
from services.PlanService import PlanService
from fastapi import Request

router = APIRouter()

@router.get('/plans')
async def get_plans():
    try:
        plans = PlanService.get_plans()
        return JSONResponse(content={'plans': [plan.dict() for plan in plans]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao obter planos: {e}'}, status_code=500)
    
@router.get('/plans/{club_id}')
async def get_plans_by_club_id(club_id: str):
    try:
        plans = PlanService.get_plans_by_club_id(club_id=club_id)
        return JSONResponse(content={'plans': [plan.dict() for plan in plans]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao obter planos: {e}'}, status_code=500)

@router.post('/createPlan')
async def create_plan(plan: RegisterPlan):
    try:
        PlanService.create_plan(plan= plan)
        return JSONResponse(content={'message': 'Plano criado com sucesso'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao criar plano: {e}'}, status_code=500)