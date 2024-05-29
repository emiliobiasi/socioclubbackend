from pydantic import BaseModel
import datetime

class Associate(BaseModel):
    id: int
    client_id: int
    plan_id: int
    end_date: datetime

    dictId = 'id'
    dictClient_id = 'client_id'
    dictPlan_id = 'plan_id'
    dictEnd_date = 'end_date'

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['eventDate'] = d['eventDate'].strftime("%Y-%m-%d %H:%M:%S")

        return d