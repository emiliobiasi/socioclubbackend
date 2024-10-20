from pydantic import BaseModel

class Vinculate(BaseModel):
    socioclub_id: str
    stripe_id: str
    price_id: str