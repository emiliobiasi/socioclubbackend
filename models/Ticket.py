from pydantic import BaseModel
from typing import ClassVar

class Ticket(BaseModel):
    qr_code:str
    event_id: int

    #String com nome dos atributos
    dictQr_code: ClassVar[str] = 'qr_code'
    dictEvent_id: ClassVar[str] = 'event_id' 

        
