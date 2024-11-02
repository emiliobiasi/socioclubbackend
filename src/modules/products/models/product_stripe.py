from pydantic import BaseModel

class ProductStripe(BaseModel):

    id: int
    name: str
    description: str
    price: float
    image: str
    category_id: int
    stripe_id: str
    price_id: str
