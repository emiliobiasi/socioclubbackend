from pydantic import BaseModel

class Vinculate(BaseModel):
    product_id: int
    event_id: int
    stripe_id: str
    price_id: str