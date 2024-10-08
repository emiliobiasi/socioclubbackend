from pydantic import BaseModel

class RegisterStripeClub(BaseModel):
    club_id: int
    stripe_id: str
