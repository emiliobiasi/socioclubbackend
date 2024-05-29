import json
from datetime import datetime
from pydantic import BaseModel
class Event(BaseModel):
    id: int
    eventName: str
    description: str
    image: str
    fullPrice: float
    eventDate: datetime
    ticketsAway: int
    ticketsHome: int
    fkClubId: int

    #String com nome dos atributos
    dictId = 'id'
    dictEventName = 'eventName'
    dictDescription = 'description'
    dictImage = 'image'
    dictFullPrice = 'fullPrice'
    dictEventDate = 'eventDate'
    dictTicketsAway = 'ticketsAway'
    dictTicketsHome = 'ticketsHome'
    dictFkClubId = 'fkClubId'


    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['eventDate'] = d['eventDate'].strftime("%Y-%m-%d %H:%M:%S")

        return d