from pydantic import BaseModel

class SetupClub(BaseModel):
    description: str
    logo: str
    background: str
    club_category: int