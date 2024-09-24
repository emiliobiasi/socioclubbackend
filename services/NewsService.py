from typing import List
from models.News import News
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class NewsService:

    @staticmethod
    def get_news() -> List[News]:
        connection = connect_to_db()

        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT id, text, image, author, title, publish_date, fk_Club_id FROM News')
            data = cursor.fetchall()
            cursor.close
            news_list = []
            for news in data:
                news_list.append(
                    News(
                        id = news[0],
                        text=news[1],
                        image=news[2],
                        author=news[3],
                        title=news[4],
                        publish_date=news[5],
                        club_id=news[6],                       
                    )
                )
            return news_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def get_news_by_club_id(club_id: str) -> List[News]:
        connection = connect_to_db()

        if connection:
            
            cursor = connection.cursor()
            cursor.execute('SELECT id, text, image, author, title, publish_date, fk_Club_id FROM News WHERE fk_Club_id = %s',(club_id))
            data = cursor.fetchall()
            cursor.close
            news_list = []
            for news in data:
                news_list.append(
                    News(
                        id = news[0],
                        text=news[1],
                        image=news[2],
                        author=news[3],
                        title=news[4],
                        publish_date=news[5],
                        club_id=news[6], 
                    )
                )
            return news_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")