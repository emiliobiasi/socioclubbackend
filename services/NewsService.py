from typing import List
from models.news.News import News
from models.news.CreateNews import CreateNews
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
            cursor.execute('SELECT id, text, image, author, fk_Club_id, publish_date, title FROM News')
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
                        club_id=news[4],                       
                        publish_date=news[5],
                        title=news[6],
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
            cursor.execute('SELECT id, text, image, author, fk_Club_id, publish_date, title FROM News WHERE fk_Club_id = %s',(club_id,))
            data = cursor.fetchall()
            cursor.close()
            news_list = []
            for news in data:
                news_list.append(
                    News(
                        id = news[0],
                        text=news[1],
                        image=news[2],
                        author=news[3],
                        club_id=news[4],                       
                        publish_date=news[5],
                        title=news[6],
                    )
                )
            return news_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
    
    @staticmethod
    def create_news(new_news: CreateNews):

        create_query = '''
            insert into news (text,image,author,title,publish_date,fk_Club_id)
            values (
                %s,
                %s,
                %s,
                %s,
                NOW(),
                %s
            ) returning id,text,image,author,title,publish_date,fk_Club_id;
        '''

        create_tuple = (new_news.text,new_news.image,new_news.author,new_news.title,new_news.club_id)

        data = NewsService._execute_select_one_query(query=create_query, t= create_tuple)

        return News(
            id=data[0],
            text=data[2],
            image=data[3],
            author=data[4],
            club_id=data[6],
            publish_date=data[5],
            title=data[1]
        )
    
    @staticmethod
    def delete_new(new_id: str):
        delete_query = "delete from news where id = %s"
        delete_tuple = (new_id,)

        NewsService._execute_query(delete_query, delete_tuple)
        
    @staticmethod
    def _execute_query(query:str, t: tuple):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, t)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def _execute_select_one_query(query: str, t: tuple):
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, t)
            data = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()

            return data
        else:
            raise Exception("Falha na conexão ao PostgreSQL")