from pydantic import BaseModel

class Ticket(BaseModel):
    qr_code:str
    event_id: int

    #String com nome dos atributos
    dictQr_code = 'qr_code'
    dictEvent_id = 'event_id' 

        
