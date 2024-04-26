from typing import List
from models.Club import Club
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

class ClubService:

    @staticmethod
    def get_clubs() -> List[Club]:
        connection = connect_to_db()
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLUBS;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            clubs_list = []
            for club in data:
                clubs_list.append(
                    Club(id=club[0], cpf=club[1], name=club[2], email=club[3], password=club[4]))
            return clubs_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")