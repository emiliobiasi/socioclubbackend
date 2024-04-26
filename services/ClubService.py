from typing import List
from models.Club import Club
from database.connection.Connection import connect_to_db
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import base64

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
                    Club(
                        name = club[1],
                        email = club[2],
                        password = club[3],
                        cnpj = club[4],
                        description = club[5],
                        address = club[6],
                        primary_color = club[7],
                        secondary_color = club[8],
                        logo = club[9].tobytes().decode('utf-8'),
                        background = club[10].tobytes().decode('utf-8'),
                    )
                    
                )
            return clubs_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")