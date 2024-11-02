from pydantic import BaseModel
from typing import ClassVar

class PlanStripe(BaseModel):
    id:int
    name: str
    description: str
    image:str
    price: float
    discount: int
    priority: int
    club_id: int
    stripe_id: str
    price_id: str

    dictId: ClassVar[str] = 'id'
    dictName: ClassVar[str] = 'name'
    dictDescription: ClassVar[str] = 'description'
    dictImage: ClassVar[str] = 'image'
    dictPrice: ClassVar[str] = 'price'
    dictDiscount: ClassVar[str] = 'discount'
    dictPriority: ClassVar[str] = 'priority'
    dictClub_id: ClassVar[str] = 'club_id'
    dictStripe_id: ClassVar[str] = 'stripe_id'
    dictPrice_id: ClassVar[str] = 'price_id'

    def to_dict(self):
        return {
            self.dictId: self.id,
            self.dictName: self.name,
            self.dictDescription: self.description,
            self.dictImage: self.image,
            self.dictPrice: self.price,
            self.dictDiscount: self.discount,
            self.dictPriority: self.priority,
            self.dictClub_id: self.club_id,
            self.dictStripe_id: self.stripe_id,
            self.dictPrice_id: self.price_id,
        }