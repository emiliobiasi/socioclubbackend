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
    dictId = 'id'
    dictName = 'name'
    dictDescription = 'description'
    dictPrice = 'price'
    dictImage = 'image'
    dictCategory_id = 'category_id'
    dictClub_id = 'club_id'