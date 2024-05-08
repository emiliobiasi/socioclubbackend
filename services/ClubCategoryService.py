from typing import List, Optional
from models.ClubCategory import ClubCategory
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

class ClubCategoryService:

    @staticmethod
    def get_club_categories() -> List[ClubCategory]:
        connection = connect_to_db()
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ClubCategory;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            categories_list = []
            for category in data:
                categories_list.append(
                    ClubCategory(
                        id = category[0],
                        name = category[1],
                    )
                )
            return categories_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")