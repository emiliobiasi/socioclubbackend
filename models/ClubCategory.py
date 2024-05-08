from pydantic import BaseModel

class ClubCategory(BaseModel):
    id: int
    name: str