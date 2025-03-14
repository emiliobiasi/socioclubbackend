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
        created_plan = PlanService.create_plan(plan= plan)

        print(created_plan)

        return JSONResponse(content={'plan': created_plan.to_dict()}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao criar plano: {e}'}, status_code=500)
    
@router.delete('/deletePlan/{plan_id}')
async def delete_plan(plan_id: str):
    try:
        data = PlanService.delete_plan(plan_id=plan_id)
        return JSONResponse(content={'message': 'plano deletado com sucesso'}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao deletar plano: {str(e)}"}, status_code=500)

@router.get('/getStripePlansByClubId/{club_id}')
async def get_products_by_club_id(club_id: str):
    try:
        plans = PlanService.get_stripe_plans_by_club_id(club_id=club_id)
        return JSONResponse(content={'plans': [plan.dict() for plan in plans]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)