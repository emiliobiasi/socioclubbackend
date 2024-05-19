from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from services.EventService import EventService


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