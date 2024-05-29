from pydantic import BaseModel

class ClubCategory(BaseModel):
    id: int
    name: str

    #String com nome dos atributos
    dictId = 'id'
    dictName = 'name'