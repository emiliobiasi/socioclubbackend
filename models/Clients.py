from pydantic import BaseModel


class Clients(BaseModel):
    cnpj: str
    nome: str
    email: str
    senha: str
