from pydantic import BaseModel

class Ticket(BaseModel):
    qr_code:str
    event_id: int

        
