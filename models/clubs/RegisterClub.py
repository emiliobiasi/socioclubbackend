from pydantic import BaseModel

class RegisterClub(BaseModel):
    name: str
    cnpj: str
    email: str
    address: str
    password: str