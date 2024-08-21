from pydantic import BaseModel
from typing import ClassVar
from typing import Optional

class Club(BaseModel):
    id: Optional[int] = None
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

    #String com nome dos atributos
    dictId: ClassVar[str] = 'id'
    dictName: ClassVar[str] = 'name'
    dictEmail: ClassVar[str] = 'email'
    dictPassword: ClassVar[str] = 'password'
    dictCnpj: ClassVar[str] = 'cnpj'
    dictDescription: ClassVar[str] = 'description'
    dictAddress: ClassVar[str] = 'address'
    dictLogo: ClassVar[str] = 'logo'
    dictBackground: ClassVar[str] = 'background'
    dictTitles_color: ClassVar[str] = 'titles_color'
    dictSubtitles_color: ClassVar[str] = 'subtitles_color'
    dictButtons_color: ClassVar[str] = 'buttons_color'
    dictPalette_1: ClassVar[str] = 'palette_1'
    dictPalette_2: ClassVar[str] = 'palette_2'
    dictPalette_3: ClassVar[str] = 'palette_3'
    dictClub_category: ClassVar[str] = 'club_category'