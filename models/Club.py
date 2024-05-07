from pydantic import BaseModel

class Club(BaseModel):
    id: int
    name: str
    email: str
    password: str
    cnpj: str
    description: str
    address: str
    logo: str
    background: str
    titles_color: str
    subtitles_color: str
    buttons_color: str
    palette_1: str
    palette_2: str
    palette_3: str
    club_category: int