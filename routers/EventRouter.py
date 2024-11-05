from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from services.EventService import EventService
from models.events.CreateEvent import CreateEvent


router = APIRouter()

@router.get('/events')
async def get_events():
    try:
        events = EventService.get_events()
        return JSONResponse(content={'events': [event.dict() for event in events]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter events: {str(e)}"}, status_code=500)


@router.get("/getEventsByClubId/{club_id}")
async def get_events_by_club_id(club_id: str):
    try:
        events = EventService.get_events_by_club_id(club_id=club_id)
        return JSONResponse(content={'events': [event.dict() for event in events]}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao obter eventos: {e}'}, status_code=200)
    
@router.post("/createEvent")
async def create_event(new_event: CreateEvent):
    try:
        EventService.create_event(new_event=new_event)
        return JSONResponse(content={'message': 'Evento criado com sucesso!'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message': f'Erro ao obter eventos: {e}'}, status_code=500)


@router.delete('/deleteEvent/{event_id}')
async def delete_event(event_id: str):
    try:
        data = EventService.delete_event(event_id=event_id)
        return JSONResponse(content={'message': 'evento deletado com sucesso'}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao deletar evento: {str(e)}"}, status_code=500)

@router.get('/getStripeEventByClubId/{club_id}')
async def get_products_by_club_id(club_id: str):
    try:
        events = EventService.get_stripe_events_by_club_id(club_id=club_id)
        return JSONResponse(content={'events': [event.dict() for event in events]}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao obter clubes: {str(e)}"}, status_code=500)