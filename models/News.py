from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: int
    text: str
    image: str
    author: str
    club_id: int
    publish_date: datetime
    title: str

    #String com nome dos atributos
    dictText = 'text'
    dictId = 'id'
    dictImage = 'image'
    dictAuthor = 'author'
    dictClub_id = 'club_id'
    dictPublish_date = 'publish_date'
    dictTitle = 'title'


    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['publish_date'] = d['publish_date'].strftime("%Y-%m-%d %H:%M:%S")

        return d