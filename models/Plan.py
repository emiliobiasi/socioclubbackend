from pydantic import BaseModel

class Plan(BaseModel):
    id:int
    name: str
    description: str
    image:str
    price: float
    discount: int
    priority: int
    club_id: int