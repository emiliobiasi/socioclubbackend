from pydantic import BaseModel
from typing import ClassVar

#remover senha dessa classe

class Club(BaseModel):
    id: int = None
    name: str
    email: str
    password: str
    cnpj: str
    description: str = None
    address: str
    logo: str = None
    background: str = None
    titles_color: str = None
    subtitles_color: str = None
    buttons_color: str = None
    palette_1: str = None
    palette_2: str = None
    palette_3: str = None
    club_category: int = None

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

    def to_json(self):
        return {
            f'{self.dictId}':self.id,
            f'{self.dictName}':self.name,
            f'{self.dictEmail}':self.email,
            f'{self.dictPassword}':self.password,
            f'{self.dictCnpj}':self.cnpj,
            f'{self.dictDescription}':self.description,
            f'{self.dictAddress}':self.address,
            f'{self.dictLogo}':self.logo,
            f'{self.dictBackground}':self.background,
            f'{self.dictTitles_color}':self.titles_color,
            f'{self.dictSubtitles_color}':self.subtitles_color,
            f'{self.dictButtons_color}':self.buttons_color,
            f'{self.dictPalette_1}':self.palette_1,
            f'{self.dictPalette_2}':self.palette_2,
            f'{self.dictPalette_3}':self.palette_3,
            f'{self.dictClub_category}':self.club_category,
        }