import json
from datetime import datetime
from pydantic import BaseModel
from typing import ClassVar

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
    dictId: ClassVar[str] = 'id'
    dictEventName: ClassVar[str] = 'eventName'
    dictDescription: ClassVar[str] = 'description'
    dictImage: ClassVar[str] = 'image'
    dictFullPrice: ClassVar[str] = 'fullPrice'
    dictEventDate: ClassVar[str] = 'eventDate'
    dictTicketsAway: ClassVar[str] = 'ticketsAway'
    dictTicketsHome: ClassVar[str] = 'ticketsHome'
    dictFkClubId: ClassVar[str] = 'fkClubId'


    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['eventDate'] = d['eventDate'].strftime("%Y-%m-%d %H:%M:%S")

        return d