
from typing import Optional
from pydantic import BaseModel

class CreateProductStripe(BaseModel):
    name: str
    price: int
    currency: str = "brl"
    interval: str = None
    stripe_account_id: str