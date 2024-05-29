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

    #String com nome dos atributos
    dictId = 'id'
    dictName = 'name'
    dictDescription = 'description'
    dictImage = 'image'
    dictPrice = 'price'
    dictDiscount = 'discount'
    dictPriority = 'priority'
    dictClub_id = 'club_id'