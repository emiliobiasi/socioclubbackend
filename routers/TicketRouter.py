from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from services.TicketService import TicketService

router = APIRouter()

@router.post('/createTicket')
async def create_ticket(request: Request):
    try:
        data = await request.json()

        TicketService.create_ticket(event_id=data['event_id'], club_id=data['club_id'], client_id=data['client_id'])
        return JSONResponse(content={'message': 'Ticket criado com sucesso!'}, status_code=201)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao criar Ticket: {str(e)}'}, status_code=500)

@router.get('/getAllTicketsByClientId/{client_id}')
async def get_all_tickets(client_id: str):
    try:
        tickets = TicketService.get_all_tickets(client_id=client_id)

        return JSONResponse(content={'message': [ticket.dict() for ticket in tickets]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao retornar tickets: {str(e)}'})
    
@router.get('/getValidTicketsByClientId/{client_id}')
async def get_valid_tickets_by_client_id(client_id: str):
    try:
        event_and_ticket = TicketService.get_valid_tickets_by_client_id(client_id=client_id)

        return JSONResponse(content={'message': event_and_ticket}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao retornar tickets: {str(e)}'}, status_code=500)