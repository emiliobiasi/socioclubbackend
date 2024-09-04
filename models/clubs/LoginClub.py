from pydantic import BaseModel

class LoginClub(BaseModel):
    email: str
    password: str