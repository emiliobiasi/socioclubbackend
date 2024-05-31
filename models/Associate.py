from pydantic import BaseModel
import datetime
from typing import ClassVar

class Associate(BaseModel):
    id: int
    client_id: int
    plan_id: int
    end_date: datetime

    dictId: ClassVar[str] = 'id'
    dictClient_id: ClassVar[str] = 'client_id'
    dictPlan_id: ClassVar[str] = 'plan_id'
    dictEnd_date: ClassVar[str] = 'end_date'

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['eventDate'] = d['eventDate'].strftime("%Y-%m-%d %H:%M:%S")

        return d