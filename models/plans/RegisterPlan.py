from pydantic import BaseModel
from typing import ClassVar

class RegisterPlan(BaseModel):
    name: str
    description: str
    image:str
    price: float
    discount: int
    priority: int
    club_id: int

    #String com nome dos atributos
    dictName: ClassVar[str] = 'name'
    dictDescription: ClassVar[str] = 'description'
    dictImage: ClassVar[str] = 'image'
    dictPrice: ClassVar[str] = 'price'
    dictDiscount: ClassVar[str] = 'discount'
    dictPriority: ClassVar[str] = 'priority'
    dictClub_id: ClassVar[str] = 'club_id'