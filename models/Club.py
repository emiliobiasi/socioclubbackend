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

    #String com nome dos atributos
    dictId = 'id'
    dictName = 'name'
    dictEmail = 'email'
    dictPassword = 'password'
    dictCnpj = 'cnpj'
    dictDescription = 'description'
    dictAddress = 'address'
    dictLogo = 'logo'
    dictBackground = 'background'
    dictTitles_color = 'titles_color'
    dictSubtitles_color = 'subtitles_color'
    dictButtons_color = 'buttons_color'
    dictPalette_1 = 'palette_1'
    dictPalette_2 = 'palette_2'
    dictPalette_3 = 'palette_3'
    dictClub_category = 'club_category'