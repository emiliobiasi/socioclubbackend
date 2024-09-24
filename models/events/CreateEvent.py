from datetime import datetime
from pydantic import BaseModel
from typing import ClassVar

class CreateEvent(BaseModel):
    eventName: str
    description: str
    image: str
    fullPrice: float
    eventDate: datetime
    ticketsAway: int
    ticketsHome: int
    fkClubId: int

    dictEventName: ClassVar[str] = 'eventName'
    dictDescription: ClassVar[str] = 'description'
    dictImage: ClassVar[str] = 'image'
    dictFullPrice: ClassVar[str] = 'fullPrice'
    dictEventDate: ClassVar[str] = 'eventDate'
    dictTicketsAway: ClassVar[str] = 'ticketsAway'
    dictTicketsHome: ClassVar[str] = 'ticketsHome'
    dictFkClubId: ClassVar[str] = 'fkClubId'