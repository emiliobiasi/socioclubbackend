from typing import List, Optional
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
        
    @staticmethod
    def find_by_id(client_id: int) -> Optional[Club]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM CLUBS WHERE id={client_id};")
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                print(data)
                return Club(
                        name = data[1],
                        email = data[2],
                        password = data[3],
                        cnpj = data[4],
                        description = data[5],
                        address = data[6],
                        primary_color = data[7],
                        secondary_color = data[8],
                        logo = data[9].tobytes().decode('utf-8'),
                        background = data[10].tobytes().decode('utf-8'),
                    )
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")