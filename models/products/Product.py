from typing import ClassVar
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category_id: int
    club_id: int

    #String com nome dos atributos
    dictId: ClassVar[str] = 'id'
    dictName: ClassVar[str] = 'name'
    dictDescription: ClassVar[str] = 'description'
    dictPrice: ClassVar[str] = 'price'
    dictImage: ClassVar[str] = 'image'
    dictCategory_id: ClassVar[str] = 'category_id'
    dictClub_id: ClassVar[str] = 'club_id'

    def to_dict(self):
        return {
            self.dictId: self.id,
            self.dictName: self.name,
            self.dictDescription: self.description,
            self.dictPrice: self.price,
            self.dictImage: self.image,
            self.dictCategory_id: self.category_id,
            self.dictClub_id: self.club_id,
        }