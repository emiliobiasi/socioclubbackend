from pydantic import BaseModel

class Club(BaseModel):
    name: str
    email: str
    password: str
    cnpj: str
    description: str
    address: str
    primary_color: str
    secondary_color: str
    logo: str
    background: str
        