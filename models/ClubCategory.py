from pydantic import BaseModel
from typing import ClassVar

class ClubCategory(BaseModel):
    id: int
    name: str

    #String com nome dos atributos
    dictId: ClassVar[str] = 'id'
    dictName: ClassVar[str] = 'name'