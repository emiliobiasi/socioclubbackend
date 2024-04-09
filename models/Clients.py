from typing import Optional
from pydantic import BaseModel


class Clients(BaseModel):
    cpf: Optional[str] = None
    name: str
    email: str
    password: str
