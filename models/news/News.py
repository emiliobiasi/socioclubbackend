from datetime import datetime
from pydantic import BaseModel
from typing import ClassVar


class News(BaseModel):
    id: int
    text: str
    image: str
    author: str
    club_id: int
    publish_date: datetime
    title: str

    #String com nome dos atributos
    dictText: ClassVar[str] = 'text'
    dictId: ClassVar[str] = 'id'
    dictImage: ClassVar[str] = 'image'
    dictAuthor: ClassVar[str] = 'author'
    dictClub_id: ClassVar[str] = 'club_id'
    dictPublish_date: ClassVar[str] = 'publish_date'
    dictTitle: ClassVar[str] = 'title'


    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['publish_date'] = d['publish_date'].strftime("%Y-%m-%d %H:%M:%S")

        return d