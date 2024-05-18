import json
from datetime import datetime
from pydantic import BaseModel
class Game(BaseModel):
    id: int
    awayTeam: str
    fullPrice: int
    gameDate: datetime
    ticketsAway: int
    ticketsHome: int
    fkClubId: int
    description: str
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['gameDate'] = d['gameDate'].strftime("%Y-%m-%d %H:%M:%S")

        return d