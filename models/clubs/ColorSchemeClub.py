from pydantic import BaseModel

class ColorSchemeClub(BaseModel):
    titles_color: str = None
    subtitles_color: str = None
    buttons_color: str = None
    palette_1: str = None
    palette_2: str = None
    palette_3: str = None