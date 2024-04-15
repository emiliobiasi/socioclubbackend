from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import Request
from services.ClientService import ClientService

from models.Client import Client


router = APIRouter()

@router.get("/clients")
async def get_clients():
    try:
        clients = ClientService.get_clients()
        return JSONResponse(content={'clients': [client.dict() for client in clients]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clientes: {str(e)}"}, status_code=500)


@router.post("/register")
async def insert_client(client: Client):
    try:
        ClientService.insert_client(client)
        return JSONResponse(content={'data': 'Cliente inserido'}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir cliente: {str(e)}")


@router.delete("/delete/{cpf}")
async def delete_client(cpf: str):
    try:
        ClientService.delete_client_by_cpf(cpf)
        return JSONResponse(content={'data': 'Cliente deletado'}, status_code=204)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")


@router.put("/update/{cpf}", response_model=Client)
async def update_client(cpf: str, client: Client):
    try:
        ClientService.update_client_by_cpf(cpf, client)
        return JSONResponse(content={'data': 'Cliente atualizado com sucesso'}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")


@router.get("/findById/{id}")
async def find_client_by_id(id: int):
    try:
        client = ClientService.find_by_id(id)
        if client:
            return JSONResponse(content={'client': client.dict()}, status_code=200)
        else:
            return JSONResponse(content={'message': 'Cliente não encontrado'}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {str(e)}")


@router.get("/findByCpf/{cpf}")
async def find_client_by_cpf(cpf: str):
    try:
        client = ClientService.find_client_by_cpf(cpf)
        if client:
            return JSONResponse(content={'client': client.dict()}, status_code=200)
        else:
            return JSONResponse(content={'message': 'Cliente não encontrado'}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {str(e)}")
    
@router.post("/login")
async def login(request: Request):
    data = await request.json()
    
    access_data = ClientService.login(email=data["email"], password=data["password"])
    
    return JSONResponse(
        content=access_data,
        status_code=status.HTTP_200_OK
    )

